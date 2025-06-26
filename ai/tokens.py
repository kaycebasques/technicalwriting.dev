from json import dump, load
from os import environ, walk
from pathlib import Path
from subprocess import run
from typing import Dict

from google.genai import Client


gemini = Client(api_key=environ["GEMINI_API_KEY"])


def _is_ignored(root: Path, target: Path, ignored: list[Path]) -> bool:
    """Check if Git is ignoring the path."""
    # Ignore Git's directory itself.
    if str(target).lower().endswith(".git"):
        return True
    # Check if this path matches something in ``.gitignore``.
    command = ["git", "-C", str(root), "check-ignore", str(target)]
    result = run(command, capture_output=True, text=True)
    return str(target) in result.stdout


def _is_in_ignored_dir(target: Path, ignored: list[Path]):
    """Check if this path is in an ignored directory."""
    for maybe_parent_dir in ignored:
        if str(maybe_parent_dir) in str(target):
            return True
    return False


def collect(root: Path) -> (list[Path], int):
    """Collect all paths in the repository."""
    paths: list[Path] = []
    ignored: list[Path] = []
    data = []
    total = 0
    for current_working_dir, _, files in walk(root):
        cwd = Path(current_working_dir)
        if _is_in_ignored_dir(cwd, ignored):
            print(f"ignoring dir: {str(cwd)}")
            continue
        if _is_ignored(Path(root), cwd, ignored):
            print(f"ignoring dir: {str(cwd)}")
            ignored.append(cwd)
            continue
        for file in files:
            path = cwd / Path(file)
            if _is_ignored(Path(root), path, ignored):
                print(f"ignoring file: {str(path)}")
                ignored.append(path)
                continue
            paths.append(path)
            with open(path, "r") as f:
                try:
                    contents = f.read()
                except UnicodeDecodeError as e:
                    continue
                print(f"counting tokens: {str(path)}")
                response = gemini.models.count_tokens(
                    model="gemini-2.5-flash", contents=contents
                )
                tokens = response.total_tokens
                total += tokens
                key = str(path)
                data.append([key, tokens])
    filenames = sorted(data, key=lambda tup: tup[0])
    filenames = [f"{x[0]}: {x[1]}" for x in filenames]
    tokens = sorted(data, key=lambda tup: tup[1], reverse=True)
    tokens = [f"{x[0]}: {x[1]}" for x in tokens]
    with open("filenames.txt", "w") as f:
        f.write("\n".join(filenames))
    with open("tokens.txt", "w") as f:
        f.write("\n".join(tokens))
    print("*" * 80)
    print(f"file count: {len(paths)}")
    print(f"tokens: {total}")


def main():
    root = Path(".")
    collect(root)


if __name__ == "__main__":
    main()
