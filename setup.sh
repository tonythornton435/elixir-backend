#!/usr/bin/env bash

sudo apt update
sudo apt install -y nginx curl tmux

# Setup Python
sudo apt install -y python3-pip libpq-dev build-essential libssl-dev libffi-dev python3-dev

# Setup virtual environment
sudo apt install -y python3-venv
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Setup Postgres
sudo apt install -y postgresql postgresql-contrib
sudo -u postgres createdb elixir
sudo -u postgres psql -c "CREATE USER elixir_user WITH PASSWORD 'x9D42Q8USGAthruU8CxD7vzxXYtmwAku';";
sudo -u postgres psql -c "ALTER ROLE elixir_user SET client_encoding TO 'utf8';";
sudo -u postgres psql -c "ALTER ROLE elixir_user SET default_transaction_isolation TO 'read committed';";
sudo -u postgres psql -c "ALTER ROLE elixir_user SET timezone TO 'UTC';";
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE elixir TO elixir_user;"
./manage.py migrate

# Populate coding tables
./manage.py runscript populate_HCPCS_table
./manage.py runscript populate_ICD10_table
./manage.py runscript populate_LOINC_table
./manage.py runscript populate_RxTerms_table

# Static
./manage.py collectstatic