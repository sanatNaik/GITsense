import os

IGNORE_DIRS = {
    "node_modules",
    ".git",
    "dist",
    "build",
    "__pycache__"
}

ALLOWED_EXT = {
    ".js", ".jsx", ".ts", ".tsx",
    ".py", ".java", ".cpp",
    ".json", ".md"
}


def chunk_file(file_path, chunk_size=100, overlap=20):
    chunks = []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except:
        return []

    start = 0
    chunk_id = 0

    while start < len(lines):
        end = min(start + chunk_size, len(lines))

        chunk_content = "".join(lines[start:end])

        chunks.append({
            "content": chunk_content,
            "file_path": file_path,
            "file_name": os.path.basename(file_path),
            "chunk_id": chunk_id
        })

        start += chunk_size - overlap
        chunk_id += 1

    return chunks


def chunk_repo(repo_path):
    all_chunks = []

    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

        for file in files:
            ext = os.path.splitext(file)[1]

            if ext not in ALLOWED_EXT:
                continue

            file_path = os.path.join(root, file)

            file_chunks = chunk_file(file_path)

            all_chunks.extend(file_chunks)

    return all_chunks