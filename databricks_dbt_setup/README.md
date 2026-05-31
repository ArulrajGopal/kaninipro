# zero_to_one_dbt

## initial setup

### create new folder -- dbt_project

cd dbt_project

sudo apt-get update

sudo apt install python3-pip


python3 -m venv .venv

source .venv/bin/activate

pip install dbt-databricks

dbt init

dbt debug
