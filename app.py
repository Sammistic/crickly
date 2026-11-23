from pathlib import Path
from flask import Flask, jsonify, render_template_string

app = Flask(__name__)
VERSION = (Path(__file__).parent / "VERSION").read_text().strip()

# (team_a, team_b, winner)
MATCHES = [
    ("Karachi Kings", "Lahore Qalandars", "Lahore Qalandars"),
    ("Islamabad United", "Karachi Kings", "Islamabad United"),
    ("Lahore Qalandars", "Islamabad United", "Lahore Qalandars"),
    ("Karachi Kings", "Islamabad United", "Karachi Kings"),
    ("Karachi Kings", "Lahore Qalandars", "Karachi Kings"),
    ("Karachi Kings", "Islamabad United", "Karachi Kings"),
]

def compute_standings(matches):
    table = {}
    for a, b, winner in matches:
        for team in (a, b):
            table.setdefault(team, {"team": team, "played": 0, "won": 0, "points": 0})
            table[team]["played"] += 1
        table[winner]["won"] += 1
        table[winner]["points"] += 2
    return sorted(table.values(), key=lambda r: (-r["points"], r["team"]))

PAGE = """
<h1>Crickly: PSL Points Table</h1>
<p><b>Table leader: {{ rows[0].team }}</b></p>
<table border="1" cellpadding="8" cellspacing="0">
  <tr><th>#</th><th>Team</th><th>Played</th><th>Won</th><th>Points</th></tr>
  {% for r in rows %}
  <tr><td>{{ loop.index }}</td><td>{{ r.team }}</td><td>{{ r.played }}</td><td>{{ r.won }}</td><td>{{ r.points }}</td></tr>
  {% endfor %}
</table>
<p><small>Matches played: {{ n }} | build v{{ version }}</small></p>
"""

@app.route("/")
def index():
    return render_template_string(PAGE, rows=compute_standings(MATCHES), n=len(MATCHES), version=VERSION)

@app.route("/api/standings")
def api_standings():
    return jsonify(compute_standings(MATCHES))

@app.route("/health")
def health():
    return jsonify(status="ok", version=VERSION)