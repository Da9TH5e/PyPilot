#tree_printer.py

def print_tree(tree: dict):
    def _walk(node, prefix=""):
        items = list(node.items())
        total = len(items)

        for index, (name, child) in enumerate(items):
            connector = "└── " if index == total - 1 else "├── "
            print(prefix + connector + name)

            if isinstance(child, dict):
                extension = "    " if index == total - 1 else "│   "
                _walk(child, prefix + extension)

    root, children = next(iter(tree.items()))
    print(root)
    _walk(children)