"""Runtime compatibility shim loaded automatically by Python at startup.

This provides a minimal torch.xpu surface for environments where the installed
PyTorch build does not expose XPU, but third-party libraries still reference it
at import time.
"""

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
