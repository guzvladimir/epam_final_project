import os

from flask import Flask, render_template, request
from launch_code import launch

app = Flask(__name__)

default = """
print("Hello world!")

name = input()
print(f'Hello {name}!')

for i in range(5):
    print(i, end=' ')
"""


@app.route("/")
@app.route("/launch", methods=["POST", "GET"])
def runpy():
    if request.method == "POST":
        code = request.form["input_code"]
        stdin = request.form["input_stdin"]
        data, temp = os.pipe()

        os.write(temp, bytes(stdin, "utf-8"))
        os.close(temp)
        run = launch.RunPythonCode(code, data)
        output_error, output = run.run_py_code()
        print(output, output_error)
        if not output:
            output = "No output"
    else:
        code = default
        output = "No output"
        output_error = "No errors"

    return render_template(
        "index.html",
        code=code,
        target="runpy",
        output=output,
        output_error=output_error,
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
