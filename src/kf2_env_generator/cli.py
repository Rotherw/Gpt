from __future__ import annotations

import argparse
from pathlib import Path

from .config import ConfigError, load_project
from .generator import GenerationError, generate_project
from .validation import ValidationError, validate_project


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a simple KF2-style environment project")
    parser.add_argument("input_path", help="Path to the JSON project definition")
    parser.add_argument("output_path", help="Path to write the generated project file")
    args = parser.parse_args()

    try:
        project = load_project(args.input_path)
        validate_project(project)
        output_path = generate_project(project, args.output_path)
    except (ConfigError, ValidationError, GenerationError) as exc:
        parser.exit(1, f"Error: {exc}\n")

    print(f"Generated environment project at {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
