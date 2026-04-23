# Team 21a

## Data Trust Engine

## Description
Our solution to the Digital Wild West.

An automated file scanning & access map generation tool designed for SMEs operating in the legal industry.

## Installation
Note that all steps bar setting up environment variables can be skipped by using the provided docker compose commands below this section
### Pre-requisites
- Clone the repository
- Install docker desktop (can be found [here](https://www.docker.com/products/docker-desktop/)) - and ensure it is open in the background
- Execute the command: `docker run --name redis-dte -d -p 6379:6379 redis:8.6.2-alpine` - this will create a docker container running a light redis container, exposed on port 6379.
This is required for the running of background processes with `Celery`

### Backend & Database Setup
This will assume a python level that is outset by university machines
- Create .env file, in the /backend folder, populating it with values from the CI/CD variables (variables where the key begins with `DOCKER` may be omitted as these are primarily for pipelines and not local running)
- Open terminal/powershell in the /backend folder.
- Execute the command `python -m venv env` - a /env folder should be created
- Activate the virtual environment in a with: `env\Scripts\activate`
- In /backend, install dependencies with `pip install -e .` - this will install dependencies from the `pyproject.toml`
- Install the spacy model with `python -m spacy download en_core_web_lg`
- All dependencies for the remaining backend setup should now be complete!
#### Database Setup
- Using `Mariadb`, ensure there is a schema named `data_trust_engine_db`
- Back in the terminal/powershell running in `/backend`, run the command `alembic upgrade head` - this will create all the tables and relations in the Database
- To populate the database with some required data and demonstrative data, run the command `Get-Content app/data.sql | mysql -u root -p data_trust_engine_db`, entering your database password as prompted.
- The Database should now be ready for the rest of the installation!
#### Celery Setup
- Open a terminal
- `cd` into the project root
- `cd` into the /backend folder
- Execute the command to run celery: `celery -A app.core.celery_worker.celery worker --pool=solo --loglevel=info --concurrency=1`
- Celery should now be connected to redis and ready for use!
#### FastAPI Server Setup
- Enter the /backend folder
- Execute the command to start the development server: `fastapi dev app\main.py`
- The FastAPI Backend server should now be running on `http://localhost:8000` and ready for calls from the frontend, which will be setup next
### Frontend Setup
- Open terminal/powershell in the projects `/frontend` directory
- Run the command `npm install` to install all frontend dependencies
- Run the command `npm run dev`
- The frontend should now be up on `http://localhost:5173/`

## Usage
### Docker Quickstart
This application is now completely dockerised, and can be run with a single docker compose command. Before running the commands below, ensure that there is a '.env' file available (keys and values can be found in the CI/CD variables - variables beginning with 'DOCKER' can be omitted) to be passed in when running profiles 'test-backend', 'dev', 'prod'.
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
    - `docker compose --env-file <path/to/.env/file> -- profile test-backend up --build`


## Support
Szymon Wodkiewicz - WodkiewiczS@cardiff.ac.uk

Oscar Webster - WebsterO1@cardiff.ac.uk

Daiyan Khan - KhanD6@cardiff.ac.uk

Samuel Carter - CarterS11@cardiff.ac.uk

Tom Clapham - ClaphamT@cardiff.ac.uk

## Roadmap
If you have ideas for releases in the future, it is a good idea to list them in the README.