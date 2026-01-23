source .env

echo "Corriendo el docker..... a la calma"
docker-compose up -d

sleep 3

docker exec -it MTG_postgres psql -U ${POSTGRES_USER} -d ${POSTGRES_DB}
