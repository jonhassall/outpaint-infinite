"""Compatibility wrapper for example.py.

Ensures torch exposes a minimal xpu attribute before diffusers imports,
then executes example.py with the same CLI arguments.
"""

import runpy
import sys

import torch


if not hasattr(torch, "xpu"):
    class _NoOp:
        def __call__(self, *args, **kwargs):
            return None

        def __getattr__(self, _name):
            return self

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

    class _XPUCompat:
        _noop = _NoOp()

        @staticmethod
        def empty_cache():
            return None

        @staticmethod
        def is_available():
            return False

        @staticmethod
        def device_count():
            return 0

        @staticmethod
        def manual_seed(_seed):
            return None

        @staticmethod
        def manual_seed_all(_seed):
            return None

        def __getattr__(self, _name):
            return self._noop

    torch.xpu = _XPUCompat()


sys.argv = ["example.py", *sys.argv[1:]]
runpy.run_path("example.py", run_name="__main__")
