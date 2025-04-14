import os
import time
import subprocess

def run_code_in_sandbox(code: str, lang: str) -> dict:
    temp_dir = f"./sandbox/temp"
    os.makedirs(temp_dir, exist_ok=True)

    lang_map = {
        "py": {"ext": "py", "file": "run.py", "docker": "sandbox_python"},
        "cpp": {"ext": "cpp", "file": "main.cpp", "docker": "sandbox_cpp"},
        "js": {"ext": "js", "file": "script.js", "docker": "sandbox_js"},
    }

    if lang not in lang_map:
        return {
            "output": "Unsupported language",
            "time": "0 sec"
        }

    target_file = lang_map[lang]["file"]
    docker_image = lang_map[lang]["docker"]

    temp_code_file = os.path.join(temp_dir, target_file)

    with open(temp_code_file, "w") as f:
        f.write(code)

    docker_cmd = [
        "docker", "run", "--rm",
        "--network=none", "--memory=128m", "--cpus=0.5",
        "-v", f"{os.path.abspath(temp_code_file)}:/sandbox/{target_file}",
        docker_image
    ]

    try:
        start_time = time.time()

        result = subprocess.run(
            docker_cmd, capture_output=True, text=True, timeout=10
        )

        execution_time = time.time() - start_time

        return {
            "output": (result.stdout or result.stderr).strip(),
            "time": f"{execution_time:.3f} sec"
        }

    except subprocess.TimeoutExpired:
        return {
            "output": "Timeout exceeded",
            "time": "10.000 sec"
        }

    except Exception as e:
        return {
            "output": f"Docker error: {str(e)}",
            "time": "0 sec"
        }
