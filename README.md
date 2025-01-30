Apenas comentários do projeto


docker ps
docker init
docker stats
docker compose up
docker compose down
docker compose up --build


docker rm imagename
docker build -t "fastzero" .
docker run -it --rm --name fastzero -p 8000:8000 fastzero:latest


alembic upgrade head
alembic init migrations
alembic revision --autogenerate -m "commentary"


gh secret set -f .env
gh repo create projectName


poetry export --without-hashes --without dev -f requirements.txt -o requirements.txt
