import os
from flask import Flask, render_template, redirect, url_for, session, jsonify
from collections import deque

app = Flask(__name__)
app.secret_key = "jug_simulation"

CAP_A = 4
CAP_B = 3
GOAL = 2


def bfs_solution():
    start = (0, 0)
    queue = deque([(start, [])])
    visited = set()

    while queue:
        (a, b), path = queue.popleft()

        if a == GOAL:
            return path + [(a, b)]

        if (a, b) in visited:
            continue
        visited.add((a, b))

        next_states = [
            (CAP_A, b), (a, CAP_B),     # Fill
            (0, b), (a, 0),             # Empty
            (a - min(a, CAP_B - b), b + min(a, CAP_B - b)),  # A → B
            (a + min(b, CAP_A - a), b - min(b, CAP_A - a))   # B → A
        ]

        for s in next_states:
            if s not in visited:
                queue.append((s, path + [(a, b)]))

    return []

def init():
    session["A"] = 0
    session["B"] = 0


@app.route("/")
def index():
    if "A" not in session:
        init()
    return render_template(
        "index.html",
        A=session["A"],
        B=session["B"],
        capA=CAP_A,
        capB=CAP_B,
        goal=GOAL
    )


@app.route("/action/<act>")
def action(act):
    A, B = session["A"], session["B"]

    if act == "fillA":
        A = CAP_A
    elif act == "fillB":
        B = CAP_B
    elif act == "emptyA":
        A = 0
    elif act == "emptyB":
        B = 0
    elif act == "pourAtoB":
        p = min(A, CAP_B - B)
        A -= p
        B += p
    elif act == "pourBtoA":
        p = min(B, CAP_A - A)
        B -= p
        A += p
    elif act == "reset":
        init()
        return redirect(url_for("index"))

    session["A"], session["B"] = A, B
    return redirect(url_for("index"))


@app.route("/solution")
def solution():
    return jsonify(bfs_solution())


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)