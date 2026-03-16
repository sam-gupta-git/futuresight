from __future__ import annotations

import importlib.util
import sysconfig
from pathlib import Path

# Preserve stdlib queue symbols (Empty, Queue, SimpleQueue, etc.) so
# third-party libraries importing `queue` keep working.
_stdlib_queue_path = Path(sysconfig.get_paths()["stdlib"]) / "queue.py"
_spec = importlib.util.spec_from_file_location("_stdlib_queue", _stdlib_queue_path)
_module = importlib.util.module_from_spec(_spec) if _spec is not None else None
if _module is not None and _spec is not None and _spec.loader is not None:
    _spec.loader.exec_module(_module)
    for _name in dir(_module):
        if _name.startswith("__"):
            continue
        globals()[_name] = getattr(_module, _name)
