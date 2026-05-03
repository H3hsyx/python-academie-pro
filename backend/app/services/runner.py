from __future__ import annotations

import ast
import os
import subprocess
import sys
import tempfile
from typing import Any

from app.core.config import get_settings


def _simulate_prints(code: str) -> dict[str, str]:
    """Simulation volontairement limitee: elle lit les print de valeurs litterales."""
    stdout: list[str] = []
    try:
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "print":
                parts: list[str] = []
                for arg in node.args:
                    try:
                        parts.append(str(ast.literal_eval(arg)))
                    except Exception:
                        parts.append("<expression>")
                stdout.append(" ".join(parts))
        return {"stdout": "\n".join(stdout), "stderr": ""}
    except SyntaxError as exc:
        return {"stdout": "", "stderr": f"SyntaxError: {exc.msg} ligne {exc.lineno}"}


def run_python_code(code: str, timeout_seconds: int = 2) -> dict[str, Any]:
    settings = get_settings()
    if not settings.enable_code_execution:
        result = _simulate_prints(code)
        result["mode"] = "simulation"
        return result

    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, encoding="utf-8") as handle:
        handle.write(code)
        filename = handle.name
    try:
        completed = subprocess.run(
            [sys.executable, "-I", filename],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=timeout_seconds,
            cwd=tempfile.gettempdir(),
        )
        return {"stdout": completed.stdout.strip(), "stderr": completed.stderr.strip(), "mode": "subprocess"}
    except subprocess.TimeoutExpired:
        return {"stdout": "", "stderr": "Temps d'execution depasse", "mode": "subprocess"}
    finally:
        try:
            os.remove(filename)
        except OSError:
            pass


def grade_stdout(stdout: str, expected_output: str) -> bool:
    return stdout.strip().replace("\r\n", "\n") == (expected_output or "").strip().replace("\r\n", "\n")
