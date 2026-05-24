from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from git import Repo
import re
import os

class RepoRequest(BaseModel):
    repourl: str

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
    ALLOWED_EXT = {".js", ".ts", ".py", ".java", ".cpp", ".json", ".md",".jsx",".tsx"}
    
	
    match = re.search(r"github\.com/([^/]+)/([^/]+?)",url)
    if match:
        author = match.group(1)
        reponame = match.group(2)
    
    local_path = r"C:\Users\Sanat\OneDrive\Desktop\GITsense\testrepo"
    
    repo_path = os.path.join(local_path,author,reponame)
    if not os.path.exists(repo_path):
        Repo.clone_from(url,repo_path)
    tree = {
        "name":reponame,
        "type":"folder",
        "children":[]
	}
    path_map = {
        os.path.join(local_path,author,reponame):tree
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
                "type":"file"
			}
            parent["children"].append(file_node)
    print(tree)
    return tree