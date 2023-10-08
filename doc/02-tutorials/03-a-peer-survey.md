# 03 - A Peer Survey

Coming soon.


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

## Create a New Section

1. [Download your course roster from Canvas](/docs/how-to/download-canvas-roster) or [create a roster](/docs/how-to/create-a-roster-file-without-canvas).
1. Create a new Spectra *section* by running `spectra new section -r <path/to/your/roster.csv> -s <section_name>`, replacing the items in `<...>` with 
your roster path and section name. The section name is up to you, but should only contain letters, numbers, dashes, and underscores.

## Define Survey Questions

Coming soon.

## Make and Share Survey Links

1. Follow instructions on [how to make a survey](/docs/how-to/make-a-survey).
1. Then run `spectra new links -i <survey.json> -s <section_name>` to generate 
group-specific links to the survey.

This will output the links to the console and generate the HTML at `spectra-data/<section_name>/outputs/<survey_name>_links.html`.


## Collect results

> **Some Manual Steps Required:** The intent is to automate these, but for now, you'll need to do the following manually:
> 
> 1. Create a directory for raw data: `mkdir -p spectra-data/<section_name>/data/surveys/raw/<survey_name>`.
> 1. Copy your survey results into that directory.
> 1. Create a directory for processed data: `mkdir -p spectra-data/<section_name>/data/surveys/proc/<survey_name>`.
>
> The following steps will be automated in the future, but as we refine the workflow, this directory
> structure may change, so we're not automating it yet.

We recommend using Canvas if it is already in use at your institution. Download zip file.
Unzip results and place in `.spectra-data/data/<section_id>/raw/<survey_name>/*.tdform`.

Survey name MUST be of the format `YYYY-MM-DD-some-name`. It MUST start with the survey collection date
in the format `YYYY-MM-DD`. This is needed by some automated indexing tools used later.


## Ingest Survey Results

1. Ingest the survey data `spectra ingest surveys -s <section_name> -i <survey_name>`

This step creates the following files in the previously created `proc` directory:

- `<survey_name>.logs.md` - A markdown summary of processing results.
- `<survey_name>.records.json` - Processed survey records for each individual question response. This
is the data that can be used for analysis or indexed with tools like Elasticsearch.
- `<survey_name>.warnings.json` - This contains processing warnings such as late or missing submissions.

The command will also output a command that can be run using PanDoc to generate a PDF report of the
processing summary. It will look something like this:

```bash
pandoc -V geometry:margin=1in spectra-data/<section_name>/data/surveys/proc/<survey_name>.logs.md -o spectra-data/<section_name>/data/surveys/proc/<survey_name>.logs.pdf
```

## Analyze Survey Results

```bash
spectra analyze SurveyReport -s <section_name> -i <survey_name>
```

In this case, `<survey_name>` is the name of the directory that was used in the raw data folder.

This step generates a Markdown report in the `spectra-data/<section_name>/outputs` directory. 

It also generates a recommended command for using [Triple Dot Engineering](https://triple.engineering)'s `evdoc` tool to generate
a PDF report. It will look something like this:

```bash
evdoc spectra-data/<section_name>/outputs/SurveyReport_<survey_name>
```

You could also generate this document using PanDoc, so we will not cover `evdoc` here.

