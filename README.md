# demo-flask-with-actions-and-kubernetes
Demo on how to use GitHub actions to deploy a python API with Flask.

### Requirements

* Python 3.7
* [Flask 2.2.3](https://flask.palletsprojects.com/en/2.2.x/). Other dependencies and packages can be checked in the `setup.py`, but they will be installed in further steps.
* Docker Desktop.
* A kubernetes cluster. If no cluster is available, [Minikube](https://minikube.sigs.k8s.io/docs/start/) could be an option.
* [git-credential-manager](https://github.com/git-ecosystem/git-credential-manager/blob/release/docs/install.md).

## Flask API

No views were created as the intention is to just create the backend. 
The API was created using flask, following the official documentation, the specific sections that were used and adapted are the following:
* [Project structure](https://flask.palletsprojects.com/en/2.2.x/tutorial/layout/)
* [Testing documentation](https://flask.palletsprojects.com/en/2.2.x/testing/)
* [Install the project](https://flask.palletsprojects.com/en/2.2.x/tutorial/install/)
* [Test Coverage - blog](https://flask.palletsprojects.com/en/2.2.x/tutorial/tests/#blog)

The app consist of a simple demo API with 2 endpoints:
* `GET https://github-flask-demo-api.com`
* `GET https://github-flask-demo-api.com/hello`

### How to call the deployed API?

The API is deployed on a Kubernetes cluster. There is no certificate or domain for the server. To be able to access it, do the following (assuming you are using macOS or Linux):

1. Open a terminal.
2. Run `sudo vi /etc/hosts` or use your favorite editor to open the file as root or a user with sudo privileges.
3. Add the following at the bottom of the file: 
   ```commandline
   #flask demo
   144.91.109.94  github-flask-demo-api.com 
   ```
4. Save it.
5. In a browser go to: `https://github-flask-demo-api.com`. A browser is the fastest way as it is just a demo API but more appropriate tools are: 
   1. `curl`.
   2. [Postman](https://www.postman.com/downloads/). 
6. Depending on your browser, you will get a certificate error that won't let you open the   

### How to start the app?

#### Terminal (Linux/macOS)

All the commands need to be run from a terminal at the root of the repository.

```commandline
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

#### What about other IDEs

Make sure to create the virtual env and install the dependencies of the project.

Then, depending on your IDE, you need to configure the commands to:

* Run: `venv/bin/flask --app flaskr run`.
* Debug: `venv/bin/flask --app flaskr run --debug`.
* Test: `pytest`.

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

For testing purposes, make sure that Docker Desktop is started to build and run the docker image with the following commands:

```commandline
docker build -t flask-demo-app:1.0 .
docker run -d -p 5000:5000 flask-demo-app:1.0
```

## GitHub actions

### self-hosted runner

A [self-hosted runner](https://docs.github.com/en/actions/hosting-your-own-runners/about-self-hosted-runners) is a system that you deploy and manage to execute jobs from GitHub Actions on GitHub.com.

#### How to create a self-hosted runner?

The runner can be installed on a server, in a local computer or use a shared runner from GitHub.

I decided to install it on a server following the instructions in the official [documentation](https://docs.github.com/en/actions/hosting-your-own-runners/adding-self-hosted-runners#adding-a-self-hosted-runner-to-an-organization).
As a future step it would be great to deploy a runner with kubernetes like in GitLab using a [gitlab-runner](https://docs.gitlab.com/runner/install/kubernetes.html) Helm chart. More details in my [GitLab repository](https://gitlab.com/devops2775/pipelines).

When Following the installation instructions the default values were used but the following:

* name of runner: `contabo`
* additional labels: `contabo`

It is recommended to install it as a [service](https://docs.github.com/en/actions/hosting-your-own-runners/configuring-the-self-hosted-runner-application-as-a-service) because with `./run.sh` it will be necessary to start the runner manually each time.

The runner will be up and running, it can be checked in the settings in GitHub: `Settings -> Actions -> Runners`.

To use the runner, use `runs-on: self-hosted` in the yaml file where the actions are defined.

##### Issues
###### Message "Must not run with sudo"
Could happen when you run the command `./config.sh --url...` to start configuring the runner. It is necessary to set the environment variable `RUNNER_ALLOW_RUNASROOT` when you execute it. 
```commandline
RUNNER_ALLOW_RUNASROOT="1" ./config.sh --url...
```

### Actions yml file

The plan is to create a workflow that will perform the following automated jobs:

* test: run the tests.
* build: build and publish the container to a registry.
* deploy: deploy the API in a kubernetes cluster.

#### Creating the yml file

The file must be created under a hidden folder called i.e. `.github/workflows/main.yml`. The folder must be at the root of the project.

GitHub provides templates available in the Actions repository under the `Actions` tab. You can also find the option to create them yourself `set up a workflow yourself` under the same tab which provides easy access to the documentation and the possibility to create it and validate it from the web.

Additional documentation for Python can be found [here](https://docs.github.com/en/actions/automating-builds-and-tests/building-and-testing-python).

##### The build action

* It was created based on [Working with the GitHub Container Registry](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry). There it is defined how to authenticate against the registry in an action, create images, push images and additional required configurations.
* In addition, this [tutorial](https://nicwortel.nl/blog/2022/continuous-deployment-to-kubernetes-with-github-actions) was used for additional set up of the action.
* About the use of variables with [contexts](https://docs.github.com/en/actions/learn-github-actions/contexts#env-context). 
* When using a GitHub default environment variable in a non script context i.e. `GITHUB_REPOSITORY` it should be used as `${{ github.repository }}`. 
* It is necessary to ensure that in `Settings -> Actions -> General` under `Work permissions` sections the `Read and write permissions` is enabled to be able to push images to the registry. 

###### Known issues

The shared runners fail to build the multi-arch images, at least the ones based on ubuntu. The self-hosted runner was able to complete the process, it could be related to the configuration of the runner or the server.

###### Improvements

The current image is being built with the tag `latest`, but it is recommended to parametrize it in order to have different versions.
Maybe a script that can extract the version from `setup.py` is the way to go?

##### WIP: The deploy action 

[Tutorial](https://nicwortel.nl/blog/2022/continuous-deployment-to-kubernetes-with-github-actions)

Before creating the deploy action we need to do additional configurations:

* The kubernetes cluster needs credentials to access the registry and pull the images.
* Create kubernetes a namespace, deployment, service and ingress yml files.

###### Kubernetes' authentication to the registry



###### Kubernetes' yml files



###### Deploy action


