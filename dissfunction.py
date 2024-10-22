import ast
import os

class FunctionAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.function_defs = set()
        self.function_calls = set()

    def visit_FunctionDef(self, node):
        # Record the function definition
        self.function_defs.add(node.name)
        self.generic_visit(node)

    def visit_Call(self, node):
        # Record the function call
        if isinstance(node.func, ast.Name):
            self.function_calls.add(node.func.id)
        self.generic_visit(node)

def find_unused_functions(directory):
    unused_functions = []
    
    # Traverse through all Python files in the given directory
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                
                with open(file_path, "r", encoding="utf-8") as f:
                    node = ast.parse(f.read(), filename=file_path)
                    analyzer = FunctionAnalyzer()
                    analyzer.visit(node)
                    
                    # Identify unused functions
                    unused = analyzer.function_defs - analyzer.function_calls
                    if unused:
                        unused_functions.append((file_path, unused))
    
    return unused_functions

if __name__ == "__main__":
    directory = input("Enter the directory path of the Python project: ")
    unused_functions = find_unused_functions(directory)

    if unused_functions:
        print("Unused functions found:")
        for file_path, functions in unused_functions:
            print(f"{file_path}: {', '.join(functions)}")
    else:
        print("No unused functions found.")
