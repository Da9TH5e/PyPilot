from pathlib import Path


class ContextBuilder:
    def __init__(self, root: Path):
        self.root = root

    def create_structure(self, path: Path) -> dict:
        node = {}

        IGNORE_DIRS = {".git", ".pypilot", "__pycache__", ".venv"}

        for item in path.iterdir():
            if item.is_symlink():
                continue

            if item.is_dir():
                if item.name in IGNORE_DIRS:
                    continue
                node[item.name] = self.create_structure(item)
            else:
                node[item.name] = None

        return node

    def build(self) -> dict:
        return {
            self.root.name: self.create_structure(self.root)
        }