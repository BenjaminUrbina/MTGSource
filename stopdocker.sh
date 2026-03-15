source .env

echo "Matando al docker...."

sleep 3
docker stop MTG_postgres
