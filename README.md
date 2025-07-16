# PoE_Ninja_Currency

Analysis of currency trends in Path Of Exile leagues.

Quickstart
1️ Clone the repo
bash

git clone https://github.com/your-org/your-repo.git
cd your-repo

2 Create and activate a virtual environment
bash

python -m venv venv
source venv/bin/activate
3 Install dependencies
bash

pip install --upgrade pip
pip install -r requirements.txt
4 Initialize the Airflow database
bash

airflow db init
5 Create an Airflow user
bash

airflow users create \
 --username admin \
 --firstname Admin \
 --lastname User \
 --role Admin \
 --email admin@example.com \
 --password admin
6 Start the webserver and scheduler
bash

airflow webserver --port 8080
airflow scheduler
Then visit http://localhost:8080 in your browser.
