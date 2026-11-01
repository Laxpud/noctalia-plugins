#!/usr/bin/env python3
"""准备登记插件的上游差异；显式 --apply 时在新分支三方应用，不提交或发布。"""

import argparse
from datetime import datetime, timezone
from pathlib import Path
import subprocess
import sys
import tomllib

ROOT = Path(__file__).resolve().parents[1]


def git(*args, **kwargs):
    """在自用仓库调用 Git；默认捕获输出，失败时停止以保留现场。"""
    return subprocess.run(["git", *args], cwd=ROOT, check=True,
                          stdout=subprocess.PIPE, **kwargs).stdout


def main():
    """先核对来源与工作区，再获取差异；仅在用户选择时修改索引和工作文件。"""
    parser = argparse.ArgumentParser(description="Prepare a plugin upstream sync.")
    parser.add_argument("plugin")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    records = tomllib.loads((ROOT / "maintenance/upstream.toml").read_text())
    if args.plugin not in records["plugins"]:
        parser.error("plugin is not registered")
    entry = records["plugins"][args.plugin]
    path = entry["path"]
    if Path(path).name != path or path.startswith("."):
        parser.error("plugin path must be a top-level directory")

    # 1. 应用前要求 main 和完全干净的工作区，避免把其他工作带进同步分支。
    if args.apply:
        if git("status", "--porcelain").strip():
            parser.error("working tree must be clean")
        if git("branch", "--show-current").strip() != b"main":
            parser.error("apply must start from main")

    # 2. 只取登记仓库的分支及基线对象；不把上游提交合并到精简仓库的历史。
    git("fetch", "--no-tags", entry["repository"], entry["branch"])
    target = git("rev-parse", "FETCH_HEAD").decode().strip()
    base = entry["revision"]
    git("fetch", "--no-tags", entry["repository"], base)
    patch = git("diff", "--binary", "--full-index", base, target, "--", path)
    manifest = tomllib.loads(git("show", f"{target}:{path}/plugin.toml").decode())
    print(f"Target revision: {target}\nUpstream version: {manifest['version']}", flush=True)
    if not patch:
        print("No plugin changes.")
        return 0
    print(git("diff", "--stat", base, target, "--", path).decode(), flush=True)
    if not args.apply:
        print("Review complete. Use --apply to prepare a sync branch.")
        return 0

    # 3. 用完整 blob ID 做三方合并。冲突保留在索引和工作树中，交给维护者处理。
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    branch = f"codex/sync-{path}-{stamp}"
    git("switch", "-c", branch)
    result = subprocess.run(["git", "apply", "--3way", "--index"],
                            cwd=ROOT, input=patch)
    print(f"Prepared branch: {branch}")
    print("Inspect git status and resolve conflicts before continuing.")
    print("After review and validation, update maintenance/upstream.toml manually.")
    return result.returncode


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except subprocess.CalledProcessError as error:
        print(f"Git command failed: {error.cmd}", file=sys.stderr)
        raise SystemExit(error.returncode)
