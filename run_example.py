"""Compatibility wrapper for example.py.

Ensures torch exposes a minimal xpu attribute before diffusers imports,
then executes example.py with the same CLI arguments.
"""

import runpy
import sys

import torch


if not hasattr(torch, "xpu"):
    class _XPUCompat:
        @staticmethod
        def empty_cache():
            return None

        @staticmethod
        def is_available():
            return False

        @staticmethod
        def device_count():
            return 0

    torch.xpu = _XPUCompat()


sys.argv = ["example.py", *sys.argv[1:]]
runpy.run_path("example.py", run_name="__main__")
