# Quick Start 

## Create a New Section

1. [Download your course roster from Canvas](/docs/how-to/download-canvas-roster) or [create a roster](/docs/how-to/create-a-roster-file-without-canvas).
1. Create a new Spectra *section* by running `spectra new section spectra new section -r <path/to/your/roster.csv> -s <section_name>`, replacing the items in `<...>` with 
your roster path and section name. The section name is up to you, but should only contain letters, numbers, dashes, and underscores.

## Generate a Survey

1. Follow instructions on [how to make a survey](/docs/how-to/make-a-survey).
1. Then run `spectra new links -i <survey.json> -s <section_name>` to generate 
group-specific links to the survey.

This will output the links to the console and generate the HTML at `spectra-data/<section_name>/outputs/<survey_name>_links.html`.