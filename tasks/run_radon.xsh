import json
uv lock
uv sync --extra test

res = json.loads($(uv run radon mi src -j))
for item in res.values():
    assert item["rank"] == "A"
