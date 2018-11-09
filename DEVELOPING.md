# Setup the Local Development

fedora-search requires Python 3.6.0+ to run. You can setup a local development environment using Python virtual environments.

Create a virtual environment

```
$ python3.6 -m venv .venv
```

Activate the virtual environment

```
$ source .venv/bin/activate
```

First upgrade pip and then install the dependencies

```
(.venv) $ pip install -U pip
(.venv) $ pip install -r requirements-dev.txt
```

### Running the tests

Before running the tests you need to have a postgres database running on your hosts. A simple way to do that it to use the postgres container.
To run this container you can install [podman](https://podman.io)

```
$ sudo dnf install podman
```

And then start the postgres container

```
$ podman run  --name database -p 5432:5432 --net=host -d postgres
```

You can run the tests with the following command.

```
$ py.test
```

You can also run all the checks (linting, format and licenses) that are validated by the CI pipeline using the tox command.

```
$ tox
```

If can then stop the postgres container using the following command


```
$ podman stop database
```

Next time you want to start the container simply run

```
$ podman start database
```
