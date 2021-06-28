# Outlier Detector Application

create/activate a virtual env

install the requirements
```bash
pip install -r requirements.txt
```

# Generating Model

Model file is too large so generate it!
run the template file to update the folder structure to download and extract the dataset
```bash
python3 template.py
```

generate the model by running all cells of jupyter notebook
generate_od.ipynb
```bash
cd /workbooks
jupyter-lab
```

# Input Data
"images/streamed_images" is the default input for the application can be updated in config as required 


# Application Setup

DB is updated with 100 units and the images are stored in thumbnails and processed directories. Skip this step or 
Initialize it after clearing the images in "images/thumbnails" and "images/processed_images/**/" directories. 

initialize the DB(sqlite3) 
```bash
python3 initialize_db.py
```

# Running Application
Running the main file will launch the application and the any *.png file found in input path(images/streamed_images/) will be moved to good or bad images path thumbnail images will be created and the DB will be updated with units status.
```bash
python3 main.py
```
use default username:root/passord:root to login or create a new one!
