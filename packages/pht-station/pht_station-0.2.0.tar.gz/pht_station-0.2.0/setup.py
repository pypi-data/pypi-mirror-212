# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['station',
 'station.app',
 'station.app.api',
 'station.app.api.api_v1',
 'station.app.api.api_v1.endpoints',
 'station.app.crud',
 'station.app.datasets',
 'station.app.db',
 'station.app.fhir',
 'station.app.models',
 'station.app.schemas',
 'station.app.tests',
 'station.app.tests.test_files',
 'station.app.trains',
 'station.app.trains.docker',
 'station.app.trains.local',
 'station.common',
 'station.common.clients',
 'station.common.clients.airflow',
 'station.common.clients.central',
 'station.common.clients.conductor',
 'station.common.clients.docker',
 'station.common.clients.fhir',
 'station.common.clients.minio',
 'station.common.clients.station',
 'station.common.clients.tests',
 'station.common.config',
 'station.common.config.tests',
 'station.ctl',
 'station.ctl.config',
 'station.ctl.fhir',
 'station.ctl.install',
 'station.ctl.tests',
 'station.scripts',
 'station.trains',
 'station.trains.local',
 'station.worker',
 'station.worker.discovery',
 'station.worker.loader',
 'station.worker.testing',
 'station.worker.trainer']

package_data = \
{'': ['*'],
 'station.ctl': ['templates/*', 'templates/authup/*', 'templates/traefik/*']}

install_requires = \
['SQLAlchemy',
 'authup>=0.5.0,<0.6.0',
 'click',
 'cryptography',
 'docker',
 'fastapi[all]',
 'fhir-kindling',
 'jinja2',
 'loguru',
 'minio',
 'numpy',
 'pandas',
 'pht-train-container-library',
 'plotly',
 'psutil',
 'psycopg2-binary',
 'pycryptodome',
 'python-keycloak',
 'python-multipart',
 'redis',
 'requests',
 'rich',
 's3fs']

entry_points = \
{'console_scripts': ['station_api = station.app.run_station:main',
                     'station_ctl = station.ctl.cli:cli']}

setup_kwargs = {
    'name': 'pht-station',
    'version': '0.2.0',
    'description': 'Python library for handling containerized PHT trains',
    'long_description': '[![Build](https://github.com/PHT-EU/station-backend/actions/workflows/Build.yml/badge.svg)](https://github.com/PHT-EU/station-backend/actions/workflows/Build.yml)\n[![Tests](https://github.com/PHT-EU/station-backend/actions/workflows/tests.yml/badge.svg)](https://github.com/PHT-EU/station-backend/actions/workflows/tests.yml)\n[![codecov](https://codecov.io/gh/PHT-Medic/station-backend/branch/master/graph/badge.svg?token=SWJRH1V44S)](https://codecov.io/gh/PHT-Medic/station-backend)\n\n# PHT Station Backend\n\nThis project contains the implementation of the station API, workers for training models, as well as the configuration\nfor the station airflow instance and related workers. A FastAPI REST API als well as a command line tool for train and\nstation management can be found in the `station` directory.\n\n## Setup development environment\n\nCheckout the repository and navigate to project directory.\n\n```bash\ngit clone https://github.com/PHT-Medic/station-backend.git\n```\n\n```bash\ncd station-backend\n```\n\n### Prerequisites\n\nMake sure the following ports required for the services are open or change the port mappings in the `docker-compose.yml`\nfile.\n\n- Postgres: `5432`\n- Redis: `6379`\n- Minio: `9000` & `9001` (Console)\n- Airflow: `8080`\n- Blaze FHIR server: `9090`\n- API: `8000`\n\n### Start services\n\nStart the services for development using docker-compose.\n\n```shell\ndocker compose up -d\n```\n\nCheck the logs of the services to see if everything is running as expected.\n\n```shell\ndocker compose logs -f\n```\n\n### Configure station config for running the API in development mode\n\nCopy the `station_config.yml.tmpl` file in the root directory to `station_config.yml` and adjust the values (especially\nconfiguring addresses and credentials for the central api)\n\n```yaml\n# Configure authentication for central services\ncentral:\n  api_url: ""\n  # Robot credentials for accessing central services, these can be obtained in the central UI\n  robot_id: "central-robot-id"\n  robot_secret: "central-robot-secret"\n  private_key: "/path/to/private_key.pem"\n  # optional password for private key\n  private_key_passphrase: "admin"\n\n######### some lines omitted #########\n\n# Configures the address and credentials for the central container registry\nregistry:\n  address:\n  password:\n  user:\n  project:\n\n```\n\n### Install python dependencies\n\nInstall dependencies using [poetry](https://python-poetry.org/). This will also create a virtual environment for the\nproject.\n\n```shell\npoetry install --with dev\n```\n\n### Run the station API\n\nTo run the station API with hot reloading, run the following command:\n\n```bash\npoetry run python station/app/run_station.py\n```\n\n\n\n   \n',
    'author': 'Michael Graf',
    'author_email': 'michael.graf@uni-tuebingen.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
