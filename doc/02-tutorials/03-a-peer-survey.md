# 03 - A Peer Survey

Coming soon.

<!--


## Create your workspace

First, create and navigate to the project directory.

```bash
mkdir sample-spectra-project
cd sample-spectra-project
```

Then, initialize the directory as a Spectra  project.

```bash
spectra init
```

## Create a course section

### Download the roster file from Canvas 

TODO

### Create the section 

```bash
spectra new section -r <path/to/your/roster.csv> --name <section-name>
```

## Create the survey

### Design the survey

TODO

### Make and share links

TODO


## Collect results

We recommend using Canvas. Download zip file.

Unzip results and place in `.spectra-data/data/<section_id>/raw/YYYY-MM-DD-your-survey-id/*.tdform`

Note, spectra uses the `YYYY-MM-DD` date format to create timestamps.

## Ingest data

Point to files on disk and run `spectra ingest --section <section_id> --survey <YYYY-MM-DD-your-survey-id>`

This will ingest the `.tdform` files and create a record (JSON object) for each question
response. All data from all the submitted forms will be stored as a single JSON
file at `.spectra-data/data/<section_id>/proc/YYYY-MM-DD-your-survey-id.json`.

Each record will look something like:

```json
{
  "dt": "YYYY-MM-DDT00:00.000Z",
  "section": "<section_id>",
  "name": "John Smith",
  "fname": "John",
  "lname": "Smith",
  "person_id": "abc123",
  "question_id" : "q1",
  "question_type": "matrix",
  "question_meta_peer_name": "Jane Doe",
  "question_meta_peer_id": "jd12345",
  "question_text": "What is the answer to this question?",
  "answer_type": "number",
  "answer_number": 4,
  "answer_text": "Foo bar baz"
}
```

## Index the results

-->