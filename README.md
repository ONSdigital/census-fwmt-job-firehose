# fwmt-job-firehose

A utility designed to send a number of jobs as fast as possible.

## Configuration

A `config.tmp.py` file exists in the root of the project. It should be filled out and copied into `instance/config.py`.

## Running

This app uses flask. Within the root of the repository, the following is sufficient:

`FLASK_APP=fwmt-job-firehose flask init-db`

`FLASK_APP=fwmt-job-firehose flask load-address-json <address json file>`

`FLASK_APP=fwmt-job-firehose flask run`

## Usage

The application will run by default on port 5000.

GET requests to `/rm/actionRequest?count=N` will return a list of `N` messages.

POST requests to `/rm/actionRequest?count=N` will send `N` messages to the configured RabbitMQ instance and return a list of IDs.
