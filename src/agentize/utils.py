import json
from pathlib import Path
from typing import Any

PathLike = str | Path


def save_text(text: str, f: PathLike) -> None:
    with Path(f).open("w", encoding="utf-8") as fp:
        fp.write(text)


def load_json(f: PathLike) -> Any:
    path = Path(f)
    if path.suffix != ".json":
        raise ValueError(f"File {f} is not a json file")

    with path.open(encoding="utf-8") as fp:
        return json.load(fp)


def save_json(data: Any, f: PathLike) -> None:
    path = Path(f)
    if path.suffix != ".json":
        raise ValueError(f"File {f} is not a json file")

    with path.open("w", encoding="utf-8") as fp:
        json.dump(data, fp, ensure_ascii=False, indent=4)
