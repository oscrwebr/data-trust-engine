# Team 21a

## Data Trust Engine

## Description
TODO
Automated file scanning & access map generation tool designed for SMEs operating in the legal industry.

## Installation
TODO

## Usage
### Docker Quickstart
This application is now completely dockerised, and can be run with a single docker compose command. Before running the commands below, ensure that there is a '.env' file available (keys and values can be found in the CI/CD variables) to be passed in when running profiles 'test-backend', 'dev', 'prod'.
#### Running a Development environment
This environment allows developers to make changes in the react frontend and fastapi backend and have these changes be synced and reflected in the running containers, meaning any changes are reflected immediately. It also rebuilds the backend application when there are changes to the pyproject.toml file, incase there is a need to add a new dependency.
##### Command
`docker compose --env-file <path/to/.env/file> --profile dev up --build --watch`
#### Running a production environment
This environment allows you to see what the production application would be like. It runs similarly to the dev environment, with fastapi and mariadb services running in a network, but this time doesn't have a react dev server. 
Instead, it builds the react application into static pages.

These pages are then served to the user via an NGINX web server running in the network. To protect the backend services, they are not port forwarded, so are inaccessible from outside the network they sit in. This is where NGINX steps in.

NGINX not only serves static files, but also acts as a reverse proxy, proxying calls to the backend, ensuring only one point of entry to the fastapi application.
#### Command
`docker compose --env-file <path/to/.env/file> -- profile prod up --build`
#### Running test environments
There are two test profiles that are used in the pipelines. The primary use of these are for pipelines, however, they are a useful tool to ensure that your code changes will pass, as they use the same base images that are used in the dev and more importantly *production* environments.
#### Commands
- Frontend:
    - `docker compose -- profile test-frontend up --build`
- Backend:
    - `docker compose --env-file <path/to/.env/file> -- profile test-frontend up --build`


## Support
Szymon Wodkiewicz - WodkiewiczS@cardiff.ac.uk

Oscar Webster - WebsterO1@cardiff.ac.uk

Daiyan Khan - KhanD6@cardiff.ac.uk

Samuel Carter - CarterS11@cardiff.ac.uk

Tom Clapham - ClaphamT@cardiff.ac.uk

## Roadmap
If you have ideas for releases in the future, it is a good idea to list them in the README.