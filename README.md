# Saas Website Monitor

A saas backend application that tracks and monitors website(s) up and down times.

## API Docs

<img width="1280" alt="saas-monitor-website" src="https://user-images.githubusercontent.com/55067204/212466106-399906fa-7795-4773-81d9-c660cb8d63f5.png">

## Features

- Monitors, detects and tracks website's up and down times
- Provides an API that responds with logs of historical stats for up and down times
- Notifies specific group of people via email (and/or SMS) when a website goes down and comes back up
- Able to perform operations all operations with the highest level of complications and sophistications applicable considered.

### The sophistication expected includes

- to track multiple websites simultaneously
- allows all common forms of authorization scheme as available on the destination server
- enforces authorization on system-system data exchange via a scheme of choice
- for data exchange interface provided to be able to return a properly encrypted analyzed historical data that is ready for use
- and every other standard SaaS software requirement

## Installation

To get it running on your local machine, follow the steps below:

1). Run the commands below in your terminal:

```bash
git clone git@github.com:aybruhm/saas-website-monitor.git
```

2). Change directory to saas-website-monitor.

3). Create a virtual environment

```bash
python -m virtualenv venv
```

4). Activate the virutal environment and Install the requirements with the command below:

```bash
source venv/bin/activate
```

```bash
pip install -r requirements.txt
```

5). Rename the `.env.template` file to `.env` and update the secret key value.

6). Run the command below to ensure that all unit tests are passing.

```python
python manage.py test
```

7). Ensure that you have redis installed on your local machine. If you have installed it, kindly start it with the command below:

```bash
redis-server
```

8). Run the development server with

```bash
python manage.py runserver
```

9). Start your celery worker in a different terminal (virtual env must be activated) session with the below command:

```python
python -m celery -A saas worker
```

10). Start your celery beat in a different terminal (virtual env must be activated) session with the below command:

```python
python -m celery -A saas beat
```

11). To keep track of your celery task progress and history. Run the command below in a different terminal session:

```python
python -m celery -A saas flower --host=127.0.0.1 --port=5588
```

12). Launch your browser and navigate to the api docs:

```http
http://127.0.0.1:8000/docs/
```
