# IMS(Inventory Management System)

An Inventory Management System(IMS) is the tool that provides user the ability to track Inventory of different infrastructures of an organisation.

## Tech Stack

- Django
- Docker, Docker-Compose
- Postgres
- Bootstrap/HTML/CSS
- Redis[Cache]
- Huey[Task Queue] 
- Nginx[Reverse Proxy]
- Graphene[GraphQL API]

## Features

- [x] User Authentication
- [x] User Registration
- [x] Admin Dashboard
  - [x] Add/Remove/Update Inventory
  - [x] Add/Remove/Update Ticket
  - [x] Add/Remove/Update Maintenance
  - [x] Report Analytics Dashboard
- [x] User Dashboard
  - [x] View Ticket and Create Ticket
- [x] Agent Dashboard
  - [x] View Ticket and Assign Ticket
  - [x] Create Activity Log

## Installation

- Fork and clone the project, and add a upstream remote to track main repo changes

```
       $ git clone git@gitlab.com:{username}/cms.git
       $ cd IMS
       $ git remote add upstream git@gitlab.com:amfoss/amfoss/ims.git
```

- Create a `.env` file in the project root directory and add the following variables

```
DEBUG=True
SECRET_KEY=secret
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DJANGO_NAME=postgres
DJANGO_USER=postgres
DJANGO_PASSWORD=postgres
```

## Docker Setup

- Install docker and docker-compose
- To run the project locally, run the following commands

* `docker-compose up -d --build` - build and run the project locally
* `docker-compose exec web python3 manage.py createsuperuser` - create admin user

For removing the docker containers, run the following command

```
    $ docker-compose down
```

- To remove all docker images, and volumes, run the following command

```
    $ docker system prune -a --volumes
```

- This will reset the database, and remove all the docker images and volumes.

- To access the admin panel, go to `http://localhost/admin/` or `http://127.0.0.1/admin/`

## Development

- For creating new features, create new branch locally and work on it.
- After testing the feature, create a PR.
- To fetch new changes

```bash
    $ git fetch upstream
    $ git rebase upstream/master
```

## Formatting

- Use `black` for formatting the code.
- `black` is already installed in the project dependencies.
- To format the code, run `black .` in the project root directory.
