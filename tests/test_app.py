import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from app import app, compute_standings

def test_compute_standings_orders_by_points():
    sample = [("A", "B", "A"), ("B", "C", "B"), ("A", "C", "A")]
    t = compute_standings(sample)
    assert (t[0]["team"], t[0]["points"]) == ("A", 4)
    assert (t[1]["team"], t[1]["points"]) == ("B", 2)
    assert t[2]["points"] == 0

def test_api_standings():
    r = app.test_client().get("/api/standings")
    assert r.status_code == 200 and len(r.json) >= 1

def test_index_renders_table():
    assert b"<table" in app.test_client().get("/").data

def test_health():
    assert app.test_client().get("/health").json["status"] == "ok"