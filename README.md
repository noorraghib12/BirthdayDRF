

1) Build pgvector container:\
**Code for building PGVECTOR CONTAINER WITH POSTGRES** \
Sample:
- sudo docker build -t drf_pgvector:latest /home/mehedi/Desktop/BirthdayDRF/drf_pgvector/

**Code for running pgvector container** 

Sample
- sudo docker volume create postgres_data 
- sudo docker run - -d -name birthday_sql -e POSTGRES_PASSWORD=password -p **POSTGRES_PORT**:5432 -v "postgres_data:/var/lib/postgresql/data" -v "./drf_pgvector/postgres/vector_extension.sql:/docker-entrypoint-initdb.d/0-vector_extension.sql" drf_pgvector:latest



2) Make custom user with superuser privileges and make changes to **.env**

CODE:
- psql -U postgres -h localhost -p **POSTGRES_PORT**
>Password: password

- CREATE ROLE **POSTGRES_NAME** WITH SUPERUSER CREATEDB CREATEROLE LOGIN ENCRYPTED PASSWORD **POSTGRES_PASSWORD**;
  


3) You wil also need to make database manually and add "**CREATE EXTENSION vector;**" in designated database. 
- psql -U **POSTGRES_NAME** -h localhost -p **POSTGRES_PORT**
- CREATE DATABASE **POSTGRES_DB**;
- \c **POSTGRES_DB**;
- CREATE EXTENSTION vector;
- exit;



4) Now build main django app docker

- sudo docker build -t django_birthday .
- sudo docker run --name djangobd_v3 --env-file .env --network=host  django_birthday:latest
