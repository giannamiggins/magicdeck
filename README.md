# Flask Rundeck Dashboard

Uses Rundeck database to visually display live updates on failed jobs

![FINSIHEDDASH](https://user-images.githubusercontent.com/49261430/62052769-2e5cbc00-b1e4-11e9-9fa8-ee709a77188d.PNG)

## Getting Started

What things you need to install the software.

*   Git
*   Python
*   Pip

## Install

Clone the git repository on your computer

```
$ git clone https://github.com/equinoxfitness/magicdeck.git
```

You can also download the entire repository as a zip file and unpack in on your computer if you do not have git

## Virtual Environment
create virtual environment named venv and activate
```
$ cd magicdeck
$ python3 -m venv venv
$ source venv/bin/activate
```
For Windows
```
$ cd magicdeck
$ virtualenv venv
$ path\to\magicdeck\venv\Scripts\activate.bat
```

After cloning the application, you need to install it's dependencies into the virtual environment
```
$ pip install -r requirements.txt
```

## Example Credentials File
must provide all four connections or delete unwanted create_engine statements in app.py and runtime.py
```
produrl = 'postgres+psycopg2://username:password@host/databasename'
qaurl = 'postgresql://username:password@host/databasename'
stagurl = 'postgresql://username:password@host/databasename'
testurl = 'postgresql://username:password@host/databasename'
```

## Run the application
 
``` 
$ set FLASK_APP=app
$ flask run
```

## Optional Hambot Dashboard
add hambot database connection to credentials file

```
hambot = 'postgresql://username:password@host/databasename'
```
if you do not want to use this feature, simply leave out the hambot connection and the app will still run

## Built With
*   [Python](https://www.python.org/) - an interpreted, high-level, general-purpose programming language
*   [Flask](http://flask.pocoo.org/) - a micro web framework written in Python based on Werkzeug and Jinja2 
*   [PostgreSQL](https://www.postgresql.org/) - the world's most advanced open source relational database
