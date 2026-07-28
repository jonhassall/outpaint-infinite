"""Runtime compatibility shim loaded automatically by Python at startup.

This provides a minimal torch.xpu surface for environments where the installed
PyTorch build does not expose XPU, but third-party libraries still reference it
at import time.
"""

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
