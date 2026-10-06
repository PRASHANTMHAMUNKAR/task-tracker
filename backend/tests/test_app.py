import app as app_module


def client():
    return app_module.create_app().test_client()


def test_health():
    res = client().get("/api/health")
    assert res.status_code == 200
    assert res.get_json() == {"status": "ok"}


def test_create_task_rejects_empty_title():
    res = client().post("/api/tasks", json={"title": "   "})
    assert res.status_code == 400


def test_create_task_rejects_long_title():
    res = client().post("/api/tasks", json={"title": "x" * 101})
    assert res.status_code == 400


def test_health_db_returns_503_when_db_down(monkeypatch):
    def boom():
        raise RuntimeError("db unreachable")

    monkeypatch.setattr(app_module, "get_conn", boom)
    res = client().get("/api/health/db")
    assert res.status_code == 503
    assert res.get_json()["database"] == "down"
