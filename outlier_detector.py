import os
import shutil
import glob
import numpy as np
from PIL import Image
from alibi_detect.utils.saving import load_detector
from db_helper import *

model_path = CWD + config["model"]["od_model"]
stream_path = CWD + config["data"]["stream_path"]
processed_good = CWD + config["data"]["processed_good"]
processed_bad = CWD + config["data"]["processed_bad"]
thumbnail_path = CWD + config["data"]["thumbnail_path"]

detector = load_detector(model_path)
id = int(fetch_last()) if fetch_last() else 0


while True:
    for i, fpath in enumerate(glob.glob(stream_path + "/*.png")):
        id += 1
        img = Image.open(fpath)
        img_arr = np.expand_dims(np.asarray(img.convert("RGB").resize((64, 64))), axis=0).astype('float') / 255.
        pred = detector.predict(img_arr, outlier_type='instance',
                                 return_instance_score=True,
                                 return_feature_score=True)
        if pred['data']['is_outlier'][0] == 1:
            update_status("Bad")
            shutil.move(fpath, f"{processed_bad}/{id}.png")
        else:
            update_status("Good")
            shutil.move(fpath, f"{processed_good}/{id}.png")
        resized_img = img.resize((140, 140))
        resized_img.save(f"{thumbnail_path}/{id}.png")
