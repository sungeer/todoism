from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

# 内存数据，仅示例用（生产请用数据库）
tasks = []
next_id = 1


@app.route("/")
def index_page():
    # 返回主页 HTML（内含 Vue）
    return render_template("index.html")


# API
@app.route("/api/tasks", methods=["GET"])
def list_tasks():
    return jsonify({"items": tasks})


@app.route("/api/tasks", methods=["POST"])
def create_task():
    global next_id
    data = request.get_json(silent=True) or {}
    body = (data.get("body") or "").strip()
    if not body:
        return jsonify({"message": "body 不能为空"}), 400
    task = {"id": next_id, "body": body, "done": False}
    next_id += 1
    tasks.append(task)
    return jsonify({"message": "创建成功", "item": task})


@app.route("/api/tasks/<int:task_id>", methods=["PATCH"])
def toggle_task(task_id):
    for t in tasks:
        if t["id"] == task_id:
            t["done"] = not t["done"]
            return jsonify({"message": "切换状态成功", "item": t})
    return jsonify({"message": "未找到任务"}), 404


@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    global tasks
    before = len(tasks)
    tasks = [t for t in tasks if t["id"] != task_id]
    if len(tasks) == before:
        return jsonify({"message": "未找到任务"}), 404
    return jsonify({"message": "删除成功"})


@app.route("/api/tasks/clear_completed", methods=["DELETE"])
def clear_completed():
    global tasks
    tasks = [t for t in tasks if not t["done"]]
    return jsonify({"message": "已清除已完成任务"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
