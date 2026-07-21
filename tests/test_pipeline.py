import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_end_to_end_pipeline(tmp_path):
    input_path = ROOT / "examples" / "sample_project.json"
    output_path = tmp_path / "generated_project.json"

    env = dict(__import__("os").environ)
    env["PYTHONPATH"] = str(ROOT / "src") + (";" if os.name == "nt" else ":") + env.get("PYTHONPATH", "")

    result = subprocess.run(
        [sys.executable, "-m", "kf2_env_generator.cli", str(input_path), str(output_path)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
        env=env,
    )

    assert result.returncode == 0, result.stderr
    generated = json.loads(output_path.read_text(encoding="utf-8"))
    assert generated["name"] == "Sample KF2 Environment"
    assert generated["rooms"][0]["id"] == "room_01"
    assert generated["spawn_points"][0]["id"] == "spawn_01"
