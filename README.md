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

initialize the DB(sqlite3) 
```bash
python3 initialize_db.py
```

# Running Application
Running the main file will launch the application and the any .png file found in input path will be moved to good or bad images path and the DB will be updated.
```bash
python3 main.py
```
use default username:root/passord:root to login or create a new one!
