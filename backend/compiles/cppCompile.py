import logging
from sandbox.run_in_docker import run_code_in_sandbox

FORBIDDEN_HEADERS = {
    "fstream", "sstream", "cstdio", "cstdlib", "cctype",
    "sys/types.h", "sys/stat.h", "fcntl.h", "unistd.h",
    "windows.h", "process.h", "pthread.h",
    "sys/socket.h", "arpa/inet.h", "netinet/in.h", "netdb.h"
}

FORBIDDEN_FUNCTIONS = {
    "system(", "popen(", "exec(", "execl(", "execlp(", "execle(", "execv(", "execvp(",
    "fork(", "vfork(", "kill(", "exit(", "_exit(", "abort(", "raise(", "sigaction(",
    "socket(", "connect(", "send(", "recv(", "bind(", "listen(", "accept(",
    "open(", "close(", "read(", "write(", "fopen(", "freopen(", "fclose(",
    "ifstream", "ofstream", "fstream"
}

MAX_OUTPUT_LENGTH = 150000

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def truncate_output(output):
    if len(output) > MAX_OUTPUT_LENGTH:
        return output[:MAX_OUTPUT_LENGTH] + "\n[The output is cut off...]"
    return output


def check_code_safety(source_code):
    for header in FORBIDDEN_HEADERS:
        if f"#include <{header}>" in source_code:
            return f"Error: Use of forbidden library {header}!"

    for func in FORBIDDEN_FUNCTIONS:
        if func in source_code:
            return f"Error: Use of prohibited function {func}!"

    return None

def run_cpp(request):
    source_code = request["source_code"]

    safety_error = check_code_safety(source_code)
    if safety_error:
        return {
            "output": safety_error,
            "status": "failed",
            "time": "0 sec"
        }

    result = run_code_in_sandbox(source_code, "cpp")

    return {
        "output": result["output"],
        "status": "finished" if "Error" not in result["output"] and "Exception" not in result["output"] else "failed",
        "time": result["time"]
    }
