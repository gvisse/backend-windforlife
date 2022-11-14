# Backend WindForLife

Backend WindForLife is a django project.

## Installation

Clone the project in a specific directory
```bash
git clone https://gitlab.com/Guims/backend-windforlife.git
```
Ensure you to have postgreSQL and python3.10 installed

Create a virtual environnement to protect other projects:
```bash
python3 -m venv <venvName>
```

Activate it on Windows:
```cmd
<venvName>\\Scripts\\activate
```

Activate it on Linux :
```bash
<venvName>/bin/activate
```

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install requirements.

```bash
cd backend-windforlife
pip install -r requirements.txt
```

Create a database :
```sql
GRANT CONNECT TO guillaume IDENTIFIED BY WindForLife_API_db;
CREATE DATABASE WindForLife_API_db OWNER guillaume;
```

Run migrations:
```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

Fill the database
```bash
python3 manage.py loaddata data
```

## Usage

Run the server:
```bash
python3 manage.py runserver
```

Run tests :
```bash
python3 manage.py test
```

## License

[MIT](https://choosealicense.com/licenses/mit/)