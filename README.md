# fwmt-job-firehose

A utility designed to send a number of jobs as fast as possible.

## Running

This app uses flask. Within the root of the project, the following is sufficient:

`FLASK_APP=fwmt-job-firehose flask init-db`
`FLASK_APP=fwmt-job-firehose flask load-address-json <address json file>`
`FLASK_APP=fwmt-job-firehose flask run`
