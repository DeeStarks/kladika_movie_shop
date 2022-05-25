# Movie Shop - API
View API docs [here](https://documenter.getpostman.com/view/14444131/Uz59Mz6k).

## Installation
### Prerequisites
- [Docker](https://www.docker.com/get-started/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Postman](https://www.getpostman.com/downloads/)

### Setup
- Clone the repository - `git clone https://github.com/DeeStarks/kladika_movie_shop.git`
- cd into the directory - `cd kladika_movie_shop`
- Run `docker-compose up -d`
- Migrate the database - `docker-compose exec web python manage.py migrate`

The application will be available at `http://localhost:8000`
