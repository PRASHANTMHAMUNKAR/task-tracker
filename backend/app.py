import os

import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, jsonify, request


def get_conn():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "appdb"),
        user=os.getenv("DB_USER", "appuser"),
        password=os.getenv("DB_PASSWORD", "apppass"),
        connect_timeout=3,
    )


def create_app():
    app = Flask(__name__)

    @app.get("/api/health")
    def health():
        return jsonify(status="ok")

    @app.get("/api/health/db")
    def health_db():
        try:
            conn = get_conn()
            conn.close()
            return jsonify(status="ok", database="up")
        except Exception as exc:
            return jsonify(status="error", database="down", detail=str(exc)), 503

    @app.get("/api/tasks")
    def list_tasks():
        conn = get_conn()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT id, title, done FROM tasks ORDER BY id")
                return jsonify(cur.fetchall())
        finally:
            conn.close()

    @app.post("/api/tasks")
    def create_task():
        data = request.get_json(silent=True) or {}
        title = str(data.get("title", "")).strip()
        if not title or len(title) > 100:
            return jsonify(error="title must be 1-100 characters"), 400
        conn = get_conn()
        try:
            with conn, conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    "INSERT INTO tasks (title) VALUES (%s) RETURNING id, title, done",
                    (title,),
                )
                return jsonify(cur.fetchone()), 201
        finally:
            conn.close()

    @app.patch("/api/tasks/<int:task_id>")
    def toggle_task(task_id):
        conn = get_conn()
        try:
            with conn, conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    "UPDATE tasks SET done = NOT done WHERE id = %s "
                    "RETURNING id, title, done",
                    (task_id,),
                )
                row = cur.fetchone()
                if row is None:
                    return jsonify(error="not found"), 404
                return jsonify(row)
        finally:
            conn.close()

    @app.delete("/api/tasks/<int:task_id>")
    def delete_task(task_id):
        conn = get_conn()
        try:
            with conn, conn.cursor() as cur:
                cur.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
                if cur.rowcount == 0:
                    return jsonify(error="not found"), 404
                return "", 204
        finally:
            conn.close()

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
