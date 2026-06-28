#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path


REQUIRED_SKILLS = [
    "evidence-to-ppt-workflow",
    "gpt-researcher",
    "ppt-master",
]


def check_install(codex_home):
    missing = []
    for skill_name in REQUIRED_SKILLS:
        skill_file = codex_home / "skills" / skill_name / "SKILL.md"
        if not skill_file.is_file():
            missing.append((skill_name, skill_file))
    return missing


def main(argv=None):
    parser = argparse.ArgumentParser(description="Check local Codex skill installation for this workflow.")
    parser.add_argument("--codex-home", default="~/.codex", help="Codex home directory. Default: ~/.codex")
    args = parser.parse_args(argv)

    codex_home = Path(args.codex_home).expanduser().resolve()
    missing = check_install(codex_home)

    if missing:
        print("FAIL install smoke check")
        for skill_name, path in missing:
            print(f"- missing skill {skill_name}: {path}")
        return 1

    print("PASS install smoke check")
    for skill_name in REQUIRED_SKILLS:
        print(f"- found {skill_name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
