# demo-flask-with-actions-and-kubernetes
Demo on how to use GitHub actions to deploy a python API with Flask.

### Requirements

* Python 3.7
* [Flask 2.2.3 ](https://flask.palletsprojects.com/en/2.2.x/). Other dependencies and packages can be checked in the `setup.py`.
* A kubernetes cluster. If no cluster is available, [Minikube](https://minikube.sigs.k8s.io/docs/start/) could be an option.
* [git-credential-manager](https://github.com/git-ecosystem/git-credential-manager/blob/release/docs/install.md).

## Flask API

No views were created as the intention is to just create the backend. 
The API was created using flask, following the official documentation, the specific sections that were used can be found in the references section. It is not a fullThe specific parts can be found in the reference.

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



# References

[Official Flask - Project structure](https://flask.palletsprojects.com/en/2.2.x/tutorial/layout/)

[Official Flask - Testing documentation](https://flask.palletsprojects.com/en/2.2.x/testing/)

[Official Flask - Install the project](https://flask.palletsprojects.com/en/2.2.x/tutorial/install/)

[Official Flask - Test Coverage - blog](https://flask.palletsprojects.com/en/2.2.x/tutorial/tests/#blog)