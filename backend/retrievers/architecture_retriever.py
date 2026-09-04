import os
import json

IGNORE_DIRS = {
    ".git",
    "node_modules",
    "venv",
    "__pycache__",
    "dist",
    "build",
    ".next",
    "vendor"
}

KEY_FILES = {
    "README.md",
    "README.rst",
    "readme.md",
    "package.json",
    "pyproject.toml",
    "requirements.txt",
    "Dockerfile",
    "docker-compose.yml",
    "go.mod",
    "Cargo.toml",
    "setup.py",
    "Gemfile"
}

IMPORTANT_NAME_HINTS = [
    "main",
    "index",
    "app",
    "server",
    "router",
    "config",
    "settings",
    "client",
    "core"
]


def get_file_tree(root_path):

    tree = []

    for dirpath, dirnames, filenames in os.walk(root_path):

        dirnames[:] = [
            d for d in dirnames
            if d not in IGNORE_DIRS
            and not d.startswith(".")
        ]

        for filename in filenames:

            full_path = os.path.join(dirpath, filename)

            relative_path = os.path.relpath(
                full_path,
                root_path
            )

            tree.append(relative_path)

    return tree


def read_key_files(root_path, file_tree):

    contents = {}

    for file_path in file_tree:

        if os.path.basename(file_path) not in KEY_FILES:
            continue

        try:

            full_path = os.path.join(
                root_path,
                file_path
            )

            with open(
                full_path,
                "r",
                encoding="utf-8",
                errors="ignore"
            ) as file:

                contents[file_path] = file.read()[:5000]

        except Exception:
            pass

    return contents


def pick_important_files(file_tree, max_files=20):

    scored = []

    for file_path in file_tree:

        depth = file_path.count(os.sep)

        name = os.path.basename(
            file_path
        ).lower()

        score = 0

        # Prefer files closer to root
        score -= depth * 2

        # Filename hints
        if any(
            hint in name
            for hint in IMPORTANT_NAME_HINTS
        ):
            score += 5

        # Common entry points
        if name in {
            "main.py",
            "index.js",
            "index.ts",
            "app.py",
            "server.js",
            "server.ts",
            "main.go"
        }:
            score += 10

        scored.append(
            (score, file_path)
        )

    scored.sort(
        key=lambda x: x[0],
        reverse=True
    )

    return [
        file_path
        for _, file_path in scored[:max_files]
    ]


def read_truncated(
    root_path,
    files,
    max_lines=80
):

    contents = {}

    for file_path in files:

        try:

            full_path = os.path.join(
                root_path,
                file_path
            )

            with open(
                full_path,
                "r",
                encoding="utf-8",
                errors="ignore"
            ) as file:

                lines = file.readlines()[:max_lines]

                contents[file_path] = "".join(lines)

        except Exception:
            pass

    return contents


def format_file_dict(file_dict):

    return "\n\n".join(
        f"--- {path} ---\n{content}"
        for path, content in file_dict.items()
    )


def build_architecture_prompt(
    file_tree,
    key_file_contents,
    important_file_contents
):

    tree_str = "\n".join(
        file_tree[:300]
    )

    prompt = f"""
You are the Architecture Agent for GitSense.

Analyze the provided repository information and produce
a high-level architecture summary.

IMPORTANT RULES:

- Do not invent information.
- Use the actual repository evidence provided.
- README files may be incomplete or outdated.
- Do not infer architecture solely from filenames.
- Use source code snippets when available.
- This is an architecture analysis, not a detailed code explanation.

FILE TREE:

{tree_str}


README / MANIFEST FILES:

{format_file_dict(key_file_contents)}


KEY SOURCE FILES (TRUNCATED):

{format_file_dict(important_file_contents)}


Produce a structured architecture summary.

Return ONLY valid JSON.

Use exactly these keys:

{{
    "purpose": "...",
    "tech_stack": [],
    "entry_points": [],
    "directory_structure": [],
    "key_modules": [],
    "notable_patterns": []
}}

The response must be valid JSON.
"""

    return prompt


def build_architecture_context(root_path):

    file_tree = get_file_tree(
        root_path
    )

    key_files = read_key_files(
        root_path,
        file_tree
    )

    important_files = pick_important_files(
        file_tree
    )

    important_contents = read_truncated(
        root_path,
        important_files
    )

    prompt = build_architecture_prompt(
        file_tree,
        key_files,
        important_contents
    )

    return prompt