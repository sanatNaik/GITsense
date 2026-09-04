import json

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from git import Repo
import re
import os


from chunking.chunker import chunk_repo
from chunking.embedder import generate_embeddings
from chunking.vectordb import store_chunks

from agents.chat_agent import chat_agent
from agents.architecture_agent import architecture_agent

class SearchRequest(BaseModel):
    session_id: str
    query: str
    
class RepoRequest(BaseModel):
    repourl: str
class FileRequest(BaseModel):
    path:str


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def root():
    return {"message":"app is running"}

@app.post("/repo")
async def root(q: RepoRequest):
    url = q.repourl
    print(url)
    IGNORE_DIRS = {"node_modules", ".git", "dist", "build", "__pycache__"}
    ALLOWED_EXT = ALLOWED_EXT = {".js",".jsx",".ts",".tsx",".py",".java",".cpp",".c",".h",".hpp",".go",".rs",".php",".rb",".swift",".json",".yaml",".yml",".toml",".xml",".html",".css",".md",".txt","ipynb"}
    
    match = re.search(r"github\.com/([^/]+)/([^/]+?)(?:\.git)?$", url)
    
        
    if not match:
        raise HTTPException(
            status_code=400,
            detail="Invalid GitHub repository URL."
        )
    author = match.group(1)
    reponame = match.group(2)
    
    local_path = os.path.join(
		os.path.dirname(__file__),
		"testrepo"
	)
        
    repo_path = os.path.join(local_path,author,reponame)
    
    if not os.path.exists(repo_path):
        try:
            Repo.clone_from(url, repo_path)

        except Exception as e:
            print("Repository clone failed:", e)

            raise HTTPException(
                status_code=400,
                detail="Repository could not be found or accessed."
            )

    tree = {
        "name":reponame,
        "type":"folder",
        "path":repo_path,
        "children":[]
    }
    path_map = {
        repo_path:tree
    }
    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        parent = path_map[root]
        for d in dirs:
            folder_path = os.path.join(root,d)
            node = {
                "name":d,
                "type":"folder",
                "children":[]
            }
            parent["children"].append(node)
            path_map[folder_path]=node
        for f in files:
            ext = os.path.splitext(f)[1]
            if ext not in ALLOWED_EXT:
                continue
            file_node = {
                "name":f,
                "type":"file",
                "path": os.path.join(root, f)
            }
            parent["children"].append(file_node)
    print("Starting chunking...")
    chunks = chunk_repo(repo_path)
    print(f"Chunks created: {len(chunks)}")

    if len(chunks) > 0:
        print("Generating embeddings...")
        texts = [chunk["content"] for chunk in chunks]
        embeddings = generate_embeddings(texts)
        print("Embeddings generated")
        print("Storing chunks...")
        store_chunks(chunks, embeddings)
        print("Chunks stored")
        
    print("Starting architecture analysis...")
    architecture = architecture_agent.analyze(repo_path)

    os.makedirs("repo_cache", exist_ok=True)

    with open(
		"repo_cache/architecture.json",
		"w",
		encoding="utf-8"
	) as f:
        json.dump(
			architecture,
			f,
			indent=2
		)

    print("Architecture saved.")
    return {
        "tree":tree,
        "architecture": architecture
	}


@app.post("/file-content")
async def get_file_content(req: FileRequest):
    try:
        with open(req.path, "r", encoding="utf-8") as file:
            content = file.read()
        return{
            "content": content
        }
    except Exception as e:
        return {
            "error":str(e)
        }
    
@app.post("/search")
async def search(req: SearchRequest):

    answer = chat_agent.chat(
        req.session_id,
        req.query
    )

    return {
        "answer": answer
    }