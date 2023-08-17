import os, pathlib, sys
import pytest

root = pathlib.Path.cwd()
function_paths = [f.path for f in os.scandir(root / "functions") if f.is_dir()]

# Loop over all the folders in /functions
for path in function_paths:
    if ".pytest_cache" in path:  # If it's the cache lets skip
        continue
    os.chdir(path)
    code = pytest.main(["tests.py"])  # Change directory, run pytest, save the exit code
    if code.value != 0:  # Anything other than 0 means we failed a test
        sys.exit(code.value)
