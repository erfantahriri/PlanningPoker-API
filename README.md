# PlanningPoker

This is an back-end API service for PlanningPoker application
This application is created to handle PlanningPoker estimating sessions of scrum agile methodology

## Addresses

* [PlanningPoker API Doc](http://82.102.10.119:8080/redoc/) 
* [PlanningPoker API](http://82.102.10.119:8080) 
* [PlanningPoker Website](http://scrumplanning.ir)
* [PlanningPoker Front-end project Github](https://github.com/erfantahriri/PlanningPoker-Front)

## requirements

For database you should install PostgreSQL:

```sh
$ sudo apt update
$ sudo apt install postgresql postgresql-contrib
$ sudo -u postgres psql
$ CREATE DATABASE db_name;
$ CREATE USER db_username WITH PASSWORD 'db_password';
$ GRANT ALL PRIVILEGES ON DATABASE db_username TO db_name;

```

Also application will need some environment variables to run:

```sh
$ export PLANNING_POKER_DB_NAME='db_name'
$ export PLANNING_POKER_DB_USER='db_username'
$ export PLANNING_POKER_DB_PASSWORD='db_password'
$ export PLANNING_POKER_DB_HOST='127.0.0.1'
$ export PLANNING_POKER_DJANGO_SECRET_KEY='django_secret_key'
$ export PLANNING_POKER_SUID_ALPHABET='suid_alphabet'

```

And We use channels and channels_layer for implement WebSocket that uses Redis as its backing store. So you should [install Docker](https://docs.docker.com/install/linux/docker-ce/ubuntu/) first and after that start a redis server with running this command:

```sh
$ docker run -p 6379:6379 -d redis:2.8

```

## Building

It is best to use the python `virtualenv` tool to build locally:

```sh
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ python manage.py runserver 0.0.0.0:8000
```

Then visit `http://0.0.0.0:8000` to view the app. Alternatively you
can use uwsgi to run the server locally.

## Get involved!

We are happy to receive PR, bug reports, fixes and other improvements.

Please report bugs via the
[github issue tracker](https://github.com/erfantahriri/PlanningPoker-API/issues).

Master [git repository](https://github.com/erfantahriri/PlanningPoker-API):

* `git clone https://github.com/erfantahriri/PlanningPoker-API`

## Licensing

This library is GPL-3.0 licenced.
