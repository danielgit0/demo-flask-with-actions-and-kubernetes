# demo-flask-with-actions-and-kubernetes
Demo on how to use GitHub actions to deploy a python API with Flask.

### Requirements

* Python 3.7
* [Flask 2.2.3 ](https://flask.palletsprojects.com/en/2.2.x/). Other dependencies and packages can be checked in the `setup.py`.
* A kubernetes cluster. If no cluster is available, [Minikube](https://minikube.sigs.k8s.io/docs/start/) could be an option.
* [git-credential-manager](https://github.com/git-ecosystem/git-credential-manager/blob/release/docs/install.md).

## Flask API

No views were created as the intention is to just create the backend. 
The API was created using flask, following the official documentation, the specific sections that were used and adapted are the following:
* [Project structure](https://flask.palletsprojects.com/en/2.2.x/tutorial/layout/)
* [Testing documentation](https://flask.palletsprojects.com/en/2.2.x/testing/)
* [Install the project](https://flask.palletsprojects.com/en/2.2.x/tutorial/install/)
* [Test Coverage - blog](https://flask.palletsprojects.com/en/2.2.x/tutorial/tests/#blog)

### How to start the app?

#### Terminal (Linux/macOS)

All the commands need to be run from a terminal at the root of the repository.

```
#create a python virtual environment. variants of the command can be with 'python3' instead of 'python'
python -m venv venv

#activate the virtual environment
source venv/bin/activate

#install
venv/bin/pip install -e .

#(optional) check that the dependencies where installed correctly
pip list

#run the tests
pytest

#run the app
venv/bin/flask --app flaskr run
```

#### PyCharm

1. Go to `Preferences -> Project:demo-flask-with-actions-and-kubernetes -> Python Interpreter` 
2. Create a new interpreter at the root of the project. 
   1. The root of the current project and the new options are normally the default.
   2. This will create the virtual environment for your local project.
3. Open the Terminal from PyCharm.
4. Run `venv/bin/pip install -e .`.
5. Run the desired run configuration: `run`, `debug` or `tests`.
   1. The run configurations are included in the repository.
   2. **WARNING**: Do not modify the run configurations.

### How to add new dependencies?

1. Add the dependency to the `install_requires` list in `setup.py`.
2. Run `pip install -e .`.

#### Why not a requirements.txt?

The tutorial from the official documentation uses it and according to [this](https://packaging.python.org/en/latest/discussions/install-requires-vs-requirements/) it is better to define the dependencies for just the project and `pip` can analyze them.

## Containerize the application

### Prerequisites

* Docker Desktop

### Dockerfile

The `Dockerfile` contents were created using the following:

1. An official Python image: [python:3.7.3-alpine3.10](https://hub.docker.com/_/python/tags?page=1&name=3.7.3). The Python version, `3.7.3`, was selected based on the locally installed Python version.
2. For security reasons, which can be improved, a user was added to the Dockerfile following [baeldung](https://www.baeldung.com/linux/docker-alpine-add-user).
3. The `wsgi.py` which is key for the deployment was created following: [Official Flask - Deploy with uwsgi](https://flask.palletsprojects.com/en/2.2.x/deploying/uwsgi/).
4. With points 2 and 3 it is possible to use the command (`CMD`) used to start the application when the container is run.

Make sure that Docker Desktop is started to build and run the docker image with the following commands:

```commandline
docker build -t flask-demo-app:1.0 .
docker run -d -p 5000:5000 flask-demo-app:1.0
```
