import os
import tempfile
from pathlib import Path
from typing import Any

import orjson


class CacheService:
    """Centralized local JSON read/write with atomic writes."""

    def read_json(self, path: Path) -> Any:
        return orjson.loads(path.read_bytes())

    def write_json(self, path: Path, data: Any) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = orjson.dumps(data, option=orjson.OPT_INDENT_2)
        # Write to a temp file in the same directory, then rename atomically.
        fd, tmp_path = tempfile.mkstemp(dir=path.parent, suffix=".tmp.json")
        try:
            with os.fdopen(fd, "wb") as f:
                f.write(payload)
            os.replace(tmp_path, path)
        except BaseException:
            os.unlink(tmp_path)
            raise

    def exists(self, path: Path) -> bool:
        return path.is_file()
