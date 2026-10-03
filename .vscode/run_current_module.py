import runpy
import sys
from pathlib import Path

workspace = Path.cwd()
path = Path(sys.argv[1])

# Make the workspace importable
sys.path.insert(0, str(workspace))

# splitlogic/exploit/main.py -> splitlogic.exploit.main
module = ".".join(path.with_suffix("").parts)

sys.argv = [str(path), *sys.argv[2:]]

runpy.run_module(module, run_name="__main__", alter_sys=True)