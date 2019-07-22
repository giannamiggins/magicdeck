# Rundeck Dashboard With Python and Flask using PostgreSQL database

Uses Rundeck database to visually display live updates on failed jobs

## Getting Started

What things you need to install the software.

* Git
* Python
* Pip

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
```
rundeckdb = 'postgres+psycopg2://username:password@host/databasename'
database2 = 'postgresql://username:password@host/databasename'
```

## Run the application
 
``` 
$ set FLASK_APP=app
$ flask run
```

## Built With
* [Python](https://www.python.org/) - a programming language that lets you work quickly and integrate systems more effectively
* [Flask](http://flask.pocoo.org/) - a microframework for Python based on Werkzeug, Jinja 2 and good intentions
