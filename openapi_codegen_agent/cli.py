"""CLI entry point for openapi-codegen-agent."""

import argparse
import os
import platform
import shutil
import sys
from pathlib import Path


def _vscode_prompts_dir() -> Path:
    system = platform.system()
    if system == "Windows":
        base = Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming"))
        return base / "Code" / "User" / "prompts"
    elif system == "Darwin":
        return Path.home() / "Library" / "Application Support" / "Code" / "User" / "prompts"
    else:  # Linux / other
        return Path.home() / ".config" / "Code" / "User" / "prompts"


def _get_agent_file() -> Path:
    return Path(__file__).parent / "agent" / "open-api-code-gen.agent.md"


def cmd_install(args: argparse.Namespace) -> int:
    src = _get_agent_file()
    if not src.exists():
        print(f"Error: bundled agent file not found at {src}", file=sys.stderr)
        return 1

    repo_path = args.test_repository_path or os.environ.get("TEST_REPOSITORY_PATH")
    if repo_path:
        dest_dir = Path(repo_path) / ".github" / "agents"
    else:
        dest_dir = _vscode_prompts_dir()
    dest_dir.mkdir(parents=True, exist_ok=True)

    dest = dest_dir / "open-api-code-gen.agent.md"
    shutil.copy2(src, dest)
    print(f"Agent prompt installed to: {dest}")
    return 0


def cmd_path(_args: argparse.Namespace) -> int:
    path = _get_agent_file()
    if not path.exists():
        print(f"Error: bundled agent file not found at {path}", file=sys.stderr)
        return 1
    print(path)
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="openapi-codegen-agent",
        description="OpenAPI CodeGen Agent — AI-driven REST API client library generator",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    p_install = subparsers.add_parser(
        "install",
        help="Install the agent prompt into the VS Code User prompts folder",
    )
    p_install.add_argument(
        "--test_repository_path",
        metavar="DIR",
        default=None,
        help="Path to the test repository; the prompt will be placed in .github/agents/ inside it (default: VS Code User prompts folder)",
    )
    p_install.set_defaults(func=cmd_install)

    p_path = subparsers.add_parser(
        "path",
        help="Print the path to the bundled agent prompt file",
    )
    p_path.set_defaults(func=cmd_path)

    args = parser.parse_args()
    sys.exit(args.func(args))


if __name__ == "__main__":
    main()
