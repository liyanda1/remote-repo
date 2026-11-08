#!/usr/bin/env python
"""Strata 命令行入口。

用法：
    python strata.py compile
    python strata.py extract <repo>
    python strata.py holes
    python strata.py impact <symbol>
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from core.cli import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())
