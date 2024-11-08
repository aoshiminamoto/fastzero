
docker ps

docker compose up
docker compose down

docker rm imagename
docker build -t "fastzero" .
docker run -it --rm --name fastzero -p 8000:8000 fastzero:latest
