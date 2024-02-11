Project Name: Property Finder

Steps to install the app:

NOTE: This app is built with python3.9 

1. Create virtual env with python3.9
```bash
virtualenv -p python3.9 property-finder-env
```
2. Activate the env
```bash
source property-finder-env/bin/activate
```
3. Make sure the pip has been upgraded
```bash
pip install --upgrade pip
```
4. Install the project dependencies.
```bash
pip install -r requirements.txt --no-cache-dir
```
5. Check the default creds provided in default database in DATABASES at `property_finder/databases.py`. Replace the given creds(default) with the local creds of your local mysql database. Please find more details here on how to setup mysql in mac: https://dev.mysql.com/doc/refman/5.7/en/macos-installation-pkg.html
6. Check if the local server is up and running (run the below command at the root dir):
```bash
python manage.py runserver
```
7. If the local server is running, migrate the tables to the local database.
```
python manage.py migrate
```
8. Once the migrations are completed. The APIs are ready to use.

POSTMAN COLLECTION:
1. AUTH collection: https://www.postman.com/winter-spaceship-107557/workspace/property-finder/collection/18975387-6184291d-47a0-4621-aaac-0a43da046e71?action=share&creator=18975387&active-environment=18975387-b9604394-f3ba-4645-a92e-e16f219d0301
2. Property Details collection: https://www.postman.com/winter-spaceship-107557/workspace/property-finder/collection/18975387-21dd2bad-b228-4f7b-b4cb-bbebfe36574a?action=share&creator=18975387&active-environment=18975387-b9604394-f3ba-4645-a92e-e16f219d0301

What is in Auth Collection?

I've created a User Model in Django, and doing session based authentication. Hence, users can register their details and they can login, and see their login information (/me/ API)

What is in Property Details collection?

Property Details collection contains APIs to Create a new property, update an existing property, List all the properties, get a property details.


Additional Information:

I've created a free-tier mysql rds instance in aws, and s3 bucket for the purpose of storing the required property information. In order to access those instances, please refer to the shared secret credential in email.


Troubleshoot with mysqlclient for mac m1 chip:
```
MYSQLCLIENT_CFLAGS="<YOUR_MYSQLCLIENT_CFLAGS_PATH>" MYSQLCLIENT_LDFLAGS="<YOUR_MYSQLCLIENT_LDFLAGS_PATH>" arch -x86_64 pip install -I  -vvv mysqlclient --no-cache-dir
```

Troubleshoot with Auth Collection with error: "CSRF Failed: CSRF token missing or incorrect."
```
If the APIs throws error, even after registration and(or) login is completed, then please delete the cookies and try again.
```

Please Note: While using the POST/PUT listings API, if the images/files are being sent in the request. Please zip the folder that contains the files(say image files). And the name of those file should be one of the choices as mentioned here: listings/constants.py -> PROPERTY_LABEL_CHOICES