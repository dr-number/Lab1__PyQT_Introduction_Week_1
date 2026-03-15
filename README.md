# Initial setup in venv
    cd /d D:\...\dir_project
    python -m venv venv
    venv\Scripts\activate
    pip3 install -r requirements.txt

# Structure porject
root
    |-- images/
    |      |-- 1_img.jpg
    |      |-- 2_img.jpg
    |      |-- n_img.jpg
    |-- venv/
    |-- .gitignore
    |-- info.json
    |-- main.py
    |-- README.md
    |-- requirements.txt

# project preparation
## 1 In the root of the project, create an images folder and fill it with images with names that will install the files in the desired order.

# Run
    D:\...\dir_project\venv\Scripts\python.exe D:\...\dir_project\main.py
