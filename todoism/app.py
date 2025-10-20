# app.py
from flask import Flask, render_template, jsonify, request, abort
from datetime import datetime
from markupsafe import escape

app = Flask(__name__)

# 模拟数据库（内存）
ARTICLES = {
    1: {
        "id": 1,
        "title": "Vue 3 + Flask：在内容页做交互增强",
        "content": "这是一篇示例文章内容。后端使用 Jinja2 渲染，前端用 Vue 负责评论与点赞的交互。",
        "likes": 3,
        "comments": [
            {
                "id": 1,
                "author": "Alice",
                "content": "写得很好！",
                "created_at": "2024-01-01 10:00:00"
            },
            {
                "id": 2,
                "author": "Bob",
                "content": "受教了～",
                "created_at": "2024-01-02 09:30:00"
            }
        ]
    }
}


def get_article_or_404(article_id: int):
    article = ARTICLES.get(article_id)
    if not article:
        abort(404)
    return article


@app.get("/")
def index():
    # 实际可列出多篇文章，这里直接跳到 id=1 的详情
    return article_detail(1)


@app.get("/article/<int:article_id>")
def article_detail(article_id: int):
    article = get_article_or_404(article_id)
    # 注意：评论列表首屏由 Jinja2 渲染，Vue 负责后续交互
    return render_template("article_detail.html", article=article)


# 获取评论列表（用于前端刷新/同步）
@app.get("/api/articles/<int:article_id>/comments")
def list_comments(article_id: int):
    article = get_article_or_404(article_id)
    return jsonify({"ok": True, "data": article["comments"]})


# 提交评论
@app.post("/api/articles/<int:article_id>/comments")
def add_comment(article_id: int):
    article = get_article_or_404(article_id)
    data = request.get_json(silent=True) or {}
    author = (data.get("author") or "").strip()
    content = (data.get("content") or "").strip()

    if not author or not content:
        return jsonify({"ok": False, "error": "author 和 content 均不能为空"}), 400
    if len(author) > 32:
        return jsonify({"ok": False, "error": "author 过长"}), 400
    if len(content) > 1000:
        return jsonify({"ok": False, "error": "content 过长"}), 400

    # 基础防注入/安全处理：后端最终渲染时会转义；这里示例中直接作为字符串存储
    safe_author = escape(author)
    safe_content = escape(content)

    new_id = (article["comments"][-1]["id"] + 1) if article["comments"] else 1
    new_comment = {
        "id": new_id,
        "author": safe_author,
        "content": safe_content,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    article["comments"].append(new_comment)
    return jsonify({"ok": True, "data": new_comment}), 201


# 点赞（简单的计数 +1）
@app.post("/api/articles/<int:article_id>/like")
def like_article(article_id: int):
    article = get_article_or_404(article_id)
    article["likes"] += 1
    return jsonify({"ok": True, "data": {"likes": article["likes"]}})


if __name__ == "__main__":
    app.run(debug=True)
