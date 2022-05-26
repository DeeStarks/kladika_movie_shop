# Movie Shop - API
View API docs [here](https://documenter.getpostman.com/view/14444131/Uz59Mz6k).

## Installation
- First, have the following tools installed:
    - [Docker](https://www.docker.com/get-started/)
    - [Docker Compose](https://docs.docker.com/compose/install/)
    - [Postman](https://www.getpostman.com/downloads/) (not required, but recommended. You can use another API client of your choice)
- Clone the repository - `git clone https://github.com/DeeStarks/kladika_movie_shop.git`
- cd into the directory - `cd kladika_movie_shop`
- Run `docker-compose up -d`
- Migrate the database - `docker-compose exec web python manage.py migrate`
- Load the `max_rent` fixture into the database - `docker-compose exec web python manage.py loaddata max_rent` (used to set initial value of the maximum number of movies a user can rent)
- Stop running - `docker-compose down`

## Running the app
- Run `docker-compose up` or `docker-compose up -d` to start the app in the background
- The application will be available at `http://localhost:8000`. 
- Test from the terminal - `curl http://localhost:8000/` (this will return a list of movies)
