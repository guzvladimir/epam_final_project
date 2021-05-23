import configparser
from subprocess import PIPE, Popen, TimeoutExpired

from flask import Flask, json, render_template, request

app = Flask(__name__)


def get_data_from_file(name: str) -> str:
    with open(f"configuration_file/{name}", "r") as file:
        return file.read()


injection = get_data_from_file("injection.txt")

config = configparser.ConfigParser()
config.read("configuration_file/config.ini")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/launch", methods=["POST"])
def launch() -> str:
    code = injection + request.form["input_code"]
    stdin = request.form["input_stdin"]
    args = [
        "python",
        "-c",
        code,
        config["blocked"]["imports"],
        config["blocked"]["functions"],
    ]

    process = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE, encoding="utf-8")

    try:
        stdout, stderr = process.communicate(stdin, timeout=5)
    except TimeoutExpired as timeout:
        return json.dumps(
            {"output": "There's an error in your program", "error": str(timeout)}
        )

    return json.dumps({"output": str(stdout), "error": str(stderr)})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
