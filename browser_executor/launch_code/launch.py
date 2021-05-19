import os
import sys
from subprocess import PIPE, Popen, TimeoutExpired


class RunPythonCode(object):
    def __init__(self, code=None, stdin=None):
        self.code = code
        self.stdin = stdin
        if not os.path.exists("input_code"):
            os.mkdir("input_code")

    def _run_py_process(self, cmd="code.py"):
        args = [sys.executable, cmd, "os", "open", "exec", "eval"]
        if self.stdin == None:

            process = Popen(
                args, stdin=PIPE, stdout=PIPE, stderr=PIPE, encoding="utf-8"
            )
        else:
            process = Popen(
                args, stdin=self.stdin, stdout=PIPE, stderr=PIPE, encoding="utf-8"
            )

        try:
            self.stdout, self.stderr = (
                process.communicate(timeout=5)[0],
                process.communicate(timeout=5)[1],
            )
        except TimeoutExpired as timeout:
            self.stdout, self.stderr = "An error occur", timeout
            return self.stdout, self.stderr

        return self.stdout, self.stderr

    def run_py_code(self, code=None):
        filename = "./input_code/code.py"
        if not code:
            code = self.code
        with open(filename, "w") as file:
            file.write(code)
        self._run_py_process(filename)
        return self.stderr, self.stdout
