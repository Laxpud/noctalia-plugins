#!/usr/bin/env python3
"""调用上游索引生成器，从清单和 Git 历史生成可安装的 catalog.toml。"""

from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parents[1]
raise SystemExit(subprocess.call(
    [sys.executable, str(root / ".github/workflows/scripts/update-catalog.py")],
    cwd=root,
))
