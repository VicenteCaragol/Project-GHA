from flask import Flask, jsonify, request

app = Flask(__name__)

_tasks: list[dict] = []
_next_id = 1


def reset_store() -> None:
    global _next_id
    _tasks.clear()
    _next_id = 1


def create_task(title: str) -> dict:
    global _next_id
    task = {"id": _next_id, "title": title, "done": False}
    _next_id += 1
    _tasks.append(task)
    return task


def get_task(task_id: int) -> dict | None:
    for task in _tasks:
        if task["id"] == task_id:
            return task
    return None


def mark_done(task_id: int) -> dict | None:
    task = get_task(task_id)
    if task is None:
        return None
    task["done"] = True
    return task


@app.get("/tasks")
def list_tasks():
    return jsonify(_tasks)


@app.post("/tasks")
def add_task():
    data = request.get_json(silent=True) or {}
    title = data.get("title", "").strip()
    if not title:
        return jsonify({"error": "title is required"}), 400
    return jsonify(create_task(title)), 201


@app.patch("/tasks/<int:task_id>")
def complete_task(task_id: int):
    task = mark_done(task_id)
    if task is None:
        return jsonify({"error": "task not found"}), 404
    return jsonify(task)


if __name__ == "__main__":
    app.run(debug=True)
