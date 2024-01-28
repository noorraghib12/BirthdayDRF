-- Create the 'vector' extension within the database that is set in the docker-compose.yml
\c birthday;
CREATE EXTENSION IF NOT EXISTS vector;