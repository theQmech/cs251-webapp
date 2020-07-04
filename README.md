CS251 WebApp Project
====================

Contributors
------------
Rupanshu Ganvir

Sumith

Shubham Goel

Setting up environment
----------------------
Ensure that `python` version is 3.7:
```
python --version
```
Create a virtual environment and activate:
```
python -m venv myenv
source myenv/bin/activate
```

Change into project root and install:
```
cd leapOfFaith
pip install -r requirements.txt
```

Usage
-----
Change into directory `leapofFaith` if not already
Before starting the application, do the following:
```
python manage.py makemigrations
python mange.py migrate
```

The app can be started by (from )
```
python manage.py runserver
```

In order to open admin page(to upload, download csv files), use "admin, admin" as credentials

References
----------
1) https://docs.djangoproject.com/en/1.8/
2) http://materializecss.com/
3) https://www.youtube.com/watch?v=3DccH9AMwFQ
