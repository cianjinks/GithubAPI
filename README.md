# Github API Data Visualization

## Media

## Running

This project requires [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/) to run.

First, clone this respository from Github and change into the cloned directory:

```
> git clone https://github.com/cianjinks/GithubAPI
> cd ./GithubAPI
```

To access Github's API, the project requires a valid Github API Token. If you don't already have one you can [create one here](https://github.com/settings/tokens). Then, place your token in a file called `gittoken.txt` in the project root directory like so:

```
> echo <your_git_token> > gittoken.txt
```

Finally, we can launch the docker container which runs the Flask webserver:

```
> docker-compose up --build
```

Navigate to http://localhost:5000/ in a web browser to view the project.

