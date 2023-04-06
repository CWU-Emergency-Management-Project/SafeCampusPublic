# SafeCampusPublic

This repository will hold the actual code and associated documentation for public release and operation of the software

### Dependencies
- Django: `pip install django`
- Django REST Framework: `pip install djangorestframework`
- Django CORS: `pip install django-cors-headers`
- Requests: `pip install requests`
- Openpyxl: `pip install openpyxl`

### How to run the webserver
Navigate to the directory where the `manage.py` file is located in a terminal and run `python manage.py runserver`

### How to set up MariaDB and connect to Django
1. Install MariaDB through either terminal or through this link https://mariadb.com/kb/en/changes-improvements-in-mariadb-106/.
2. Once downloaded, move emergencydb folder to Program Files -> MariaDB 10.6 -> data.
3. Go terminal and set directory to `cd Program Files\MariaDB 10.6\bin`.
4. use `-u root -p` then use password set when installing MariaDB.
5. Open another terminal and set directory to where the `manage.py` in the EmergencyManagement folder.
6. use `python manage.py migrate` to transfer the current tables to MariaDB.

### How to change the Secret Key used for hashing
1. Navigate to EmergencyManagement/EmergencyManagement/
2. Open the `settings.py` file
3. Change the `SECRET_KEY` variable string created on line 23
4. Save the `settings.py` file
### IMPORTANT NOTE: Do not share this key publicily, this key is used for hashing the stored user passwords for logins. Make sure to change it before deploying the server!

