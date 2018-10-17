## NYU DevOps-Promotions Fall 2018
[![codecov](https://codecov.io/gh/nyu-promotions-f18/promotions/branch/master/graph/badge.svg)](https://codecov.io/gh/nyu-promotions-f18/promotions)

This repository consists of the source code for a RESTFUL promotions service using Python Flask.

## What's featured in the project?
    * app/service.py -- the main service built using Python Flask
    * app/models.py -- the database models
    * tests/test_service.py -- test cases using Unit test
    * tests/test_models.py -- test cases using just the Promotions model

## Endpoints of the Service
    * / - Renders the index page, methods=['GET']
    * /health - Returns the health status of the service as a json, methods=['GET']
    * /promotions - Returns a list of all the Promotions, methods=['GET']
    * /promotions/<int:promotion_id> - Returns a single Promotion based on it's id, methods=['GET']
    * /promotions - Creates a new promotion based on the data in the request body and saves it into the db, methods=['POST']
    * /promotions/<int:promotion_id> - Updates a Promotion based the body that is posted, methods=['PUT']
    * /promotions/<int:promotion_id> - Deletes a Promotion based the id specified in the path, methods=['DELETE']
    * /promotions/unavailable - Deletes all unavailable Promotions, methods=['DELETE']

## Prerequisite Installation using Vagrant

The easiest way to use this lab is with Vagrant and VirtualBox. if you don't have this software the first step is down download and install it.

Download [VirtualBox](https://www.virtualbox.org/)

Download [Vagrant](https://www.vagrantup.com/)

Clone the project to your development folder and create your Vagrant vm

```sh
    git clone https://github.com/nyu-promotions-f18/promotions.git
    cd promotions
    vagrant up
```

Once the VM is up you can use it with:

```sh
    vagrant ssh
    cd /vagrant
    python run.py
```

You should now be able to see the service running in your browser by going to
[http://localhost:5000](http://localhost:5001) or [http://192.168.33.10:5000](http://192.168.33.10:5000). You will see a message about the
service which looks something like this:

```
{
    name: "Promotions REST API Service",
    url: "http://localhost:5000/",
    version: "1.0"
}
```

When you are done, you can use `Ctrl+C` within the VM to stop the server.

## Alternative starting of the service

For running the service during development and debugging, you can also run the server
using the `flask` command with:

```sh
    export FLASK_APP=app/service.py
    flask run -h 0.0.0.0
```

or you can specify this all on one line with:

```
    env FLASK_APP=app/service.py flask run -h 0.0.0.0
```

Note that we need to bind the host IP address with `-h 0.0.0.0` so that the forwarded ports work correctly in **Vagrant**. If you were running this locally on your own computer you would not need this extra parameter.

Finally you can use the `honcho` command to start `gunicorn` to run the service with:

```sh
    honcho start
```

**Honcho** uses the `Procfile` to determine how to run the service. This file uses **Gunicorn** which is how you would start the server in production.

## Testing

Run the tests suite with:

```sh
    nosetests
```

You should see all of the tests passing with a code coverage report at the end. this is controlled by the `setup.cfg` file in the repo.

## Shutdown

When you are done, you can use the `exit` command to get out of the virtual machine just as if it were a remote server and shut down the vm with the following:

```sh
    exit
    vagrant halt
```

If the VM is no longer needed you can remove it with from your computer to free up disk space with:

```sh
    vagrant destroy
```

This repo is the student's code contribution as a part of the NYU masters class: **CSCI-GA.2820-001 DevOps and Agile Methodologies** by John Rofrano.
