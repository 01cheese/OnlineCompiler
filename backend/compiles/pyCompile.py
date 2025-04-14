import ast
import logging

from sandbox.run_in_docker import run_code_in_sandbox

FORBIDDEN_IMPORTS = {"os", "sys", "subprocess", "pathlib", "socket", "shutil", "threading"}

def check_python_ast(source_code: str) -> str | None:
    try:
        tree = ast.parse(source_code)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name.split(".")[0] in FORBIDDEN_IMPORTS:
                        return f"Forbidden module: {alias.name}"
            elif isinstance(node, ast.ImportFrom):
                if node.module and node.module.split(".")[0] in FORBIDDEN_IMPORTS:
                    return f"Prohibited import from module: {node.module}"
            elif isinstance(node, ast.Call):
                if hasattr(node.func, 'id') and node.func.id in {"eval", "exec", "__import__"}:
                    return f"Forbidden function: {node.func.id}()"
    except Exception as e:
        return f"Error parsing code: {str(e)}"
    return None

MAX_OUTPUT_LENGTH = 150000

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def truncate_output(output):
    if len(output) > MAX_OUTPUT_LENGTH:
        return output[:MAX_OUTPUT_LENGTH] + "\n[The output is cut off...]"
    return output

def check_code_safety(source_code):
    if any(module in source_code for module in FORBIDDEN_IMPORTS):
        return "Error: Using prohibited modules!"
    if "eval(" in source_code or "exec(" in source_code:
        return "Error: Using eval() and exec() is prohibited!"
    return None


def run_py(request):
    source_code = request["source_code"]

    safety_error = check_python_ast(source_code)
    if safety_error:
        return {
            "output": safety_error,
            "status": "failed",
            "time": "0 sec"
        }

    result = run_code_in_sandbox(source_code, "py")

    return {
        "output": result["output"],
        "status": "finished" if "Error" not in result["output"] and "Exception" not in result["output"] else "failed",
        "time": result["time"]
    }
