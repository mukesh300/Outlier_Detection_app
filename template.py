import os
import urllib.request
import tarfile
from initialize_db import read_params, CWD
config = read_params()

dirs = ["workbooks",
        os.path.join("workbooks", "datasets"),
        os.path.join("workbooks", "model")
        ]

files = [
        os.path.join("workbooks/datasets", "capsule.tar.xz")
        ]

for dir_ in dirs:
    os.makedirs(dir_, exist_ok=True)
    with open(os.path.join(dir_, ".gitkeep"), "w") as f:
        pass

for file_ in files:
    with open(file_, "w") as f:
        pass

url = CWD + config["DB"]["sqlite3"]
target_path = CWD + '/workbooks/datasets/capsule.tar.xz'
urllib.request.urlretrieve(url, target_path)

file = tarfile.open(target_path)
file.extractall(CWD + '/workbooks')
file.close()

