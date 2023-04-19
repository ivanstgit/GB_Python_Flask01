poetry export --without-hashes --format=requirements.txt > requirements.txt
sudo docker-compose build app
sudo docker-compose up app

first time:
sudo docker exec -it blog_app_1 flask create-users
sudo docker exec -it blog_app_1 flask create-tags

model changed:
sudo docker exec -it blog_app_1 flask db upgrade
