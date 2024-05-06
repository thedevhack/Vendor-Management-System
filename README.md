## Steps To Run the Project

1. Run the Command to clone the repo
```bash
git clone https://github.com/thedevhack/Vendor-Management-System.git
```
2. Create the environment of Python depending on your Operating System
```bash
virtualenv venv - Linux
```
```bash
python -m venv venv - Windows
```
3. Activate the Virtual Environment
```bash
source venv/bin/activate - Linux
```
```bash
venv\Scripts\activate - Windows
```
4. Pip install all the python modules required using pip
```bash
pip install -r requirements.txt
```
5. Make migrations
```bash
python manage.py migrate
```
6. Run the django server on 127.0.0.1:8000
```bash
python manage.py runserver
```
