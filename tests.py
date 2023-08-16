import os, pathlib, sys
import pytest

root = pathlib.Path.cwd()
function_paths = [f.path for f in os.scandir(root / "functions") if f.is_dir()]

for path in function_paths:
    if ".pytest_cache" in path:
        continue
    os.chdir(path)
    code = pytest.main(["tests.py"])
    if code.value != 0:
        sys.exit(code.value)
