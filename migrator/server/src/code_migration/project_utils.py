import ast
import os
import networkx as nx

def get_project_files_contents(project_path):
    files_contents = {}
    for root, _, files in os.walk(project_path):
        for file in files:
            path = os.path.join(root, file)
            with open(path, "r") as f:
                try:
                    content = f.read()
                    files_contents[path] = content
                except:
                    continue

    return files_contents

def get_project_structure(project_path, prefix=''):
    """
    Generate a string representation of the directory tree.
    
    Parameters:
    - root_dir: The root directory to generate the tree from.
    - prefix: The prefix used for the current level of the tree.
    
    Returns:
    - A string representing the tree structure.
    """
    tree_str = ''
    # Ensure the root directory ends with a slash
    if not project_path.endswith(os.sep):
        project_path += os.sep
    # Get the list of files and directories at this level
    items = sorted(os.listdir(project_path))
    for index, item in enumerate(items):
        # Determine the path to the item
        path = os.path.join(project_path, item)
        # Determine if this is the last item in the list
        is_last = (index == (len(items) - 1))
        # Add the tree branch symbol
        tree_str += prefix + ('└── ' if is_last else '├── ') + item + '\n'
        # If the item is a directory, recursively generate its tree
        if os.path.isdir(path):
            # Update the prefix for the next level based on whether this item is last
            next_prefix = prefix + ('    ' if is_last else '│   ')
            tree_str += get_project_structure(path, prefix=next_prefix)
    return tree_str

def find_file_with_name(root_dir, filename):
    """
    Search for the first file within the project directory that matches the given filename.
    """
    filename = f"{filename}.py"
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file == filename:
                return os.path.join(root, file)
    return None

def parse_imports(file_path):
    """Parse a Python file to find all imported modules and attempt to resolve their paths."""
    with open(file_path, 'r', encoding='utf-8') as file:
        node = ast.parse(file.read(), filename=file_path)
    for item in node.body:
        if isinstance(item, (ast.Import, ast.ImportFrom)):
            module_name = item.module if isinstance(item, ast.ImportFrom) else None
            for alias in item.names:
                # Handle 'import module' and 'from package import module' differently
                name = module_name or alias.name
                yield name

def find_file_dependencies(root_dir):
    """Build a dependency graph of Python files within the specified directory, resolving imports to paths."""
    G = nx.DiGraph()
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                G.add_node(file_path)
                for imported_module in parse_imports(file_path):
                    module_path = find_file_with_name(root_dir, imported_module)
                    if module_path:
                        G.add_edge(file_path, module_path)
    return G