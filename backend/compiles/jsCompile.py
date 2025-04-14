import logging
from sandbox.run_in_docker import run_code_in_sandbox

FORBIDDEN_MODULES = {"fs", "child_process", "os", "process", "path", "net", "http"}
MAX_OUTPUT_LENGTH = 150000

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def truncate_output(output):
    if len(output) > MAX_OUTPUT_LENGTH:
        return output[:MAX_OUTPUT_LENGTH] + "\n[The output is cut off...]"
    return output

def check_code_safety(source_code):
    if any(module in source_code for module in FORBIDDEN_MODULES):
        return "Error: Using prohibited modules!"
    if "require(" in source_code or "import " in source_code:
        return "Error: Use of `require()` and `import` is not allowed!"
    if "eval(" in source_code:
        return "Error: Use of `eval()` is prohibited!"
    return None

def run_js(request):
    source_code = request["source_code"]

    safety_error = check_code_safety(source_code)
    if safety_error:
        return {
            "output": safety_error,
            "status": "failed",
            "time": "0 sec"
        }

    result = run_code_in_sandbox(source_code, "js")

    return {
        "output": result["output"],
        "status": "finished" if "Error" not in result["output"] and "Exception" not in result["output"] else "failed",
        "time": result["time"]
    }
