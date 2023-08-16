import os, pathlib
import pytest

root = pathlib.Path.cwd()
function_paths = [f.path for f in os.scandir(root / "functions") if f.is_dir()]

for path in function_paths:
    if ".pytest_cache" in path:
        continue
    os.chdir(path)
    pytest.main(["tests.py"])
