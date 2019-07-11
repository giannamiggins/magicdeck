# Rundeck Dashboard With Python and Pusher

Uses Rundeck database to display job failures for each project

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

## Prerequisites

What things you need to install the software.

* Git.
* Python.
* Pip.

## Install

Clone the git repository on your computer

```
$ git clone https://github.com/equinoxfitness/magicdeck.git
```

You can also download the entire repository as a zip file and unpack in on your computer if you do not have git

After cloning the application, you need to install it's dependencies from requirements.txt and set up a virtual environment.
Credentials file should have url for database: 'postgres+psycopg2://username:password@host/databasename
   and optional pusher login information
 
```
$ cd magicdeck
$ pip install flask
$ pip install pusher
$ python dbsetup.py```
$ export FLASK_ENV=development
```

## Run the application
 
``` $ flask run```

## Built With

* [Pusher](https://pusher.com/) - Hosted APIs to build realtime apps with less code
* [Python](https://www.python.org/) - a programming language that lets you work quickly and integrate systems more effectively
* [Flask](http://flask.pocoo.org/) - a microframework for Python based on Werkzeug, Jinja 2 and good intentions
