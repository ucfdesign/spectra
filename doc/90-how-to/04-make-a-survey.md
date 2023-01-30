# Make a Survey

You can create three types of surveys.

1. Simple surveys
1. Matrix surveys
1. Peer surveys

## Simple Surveys

*Simple surveys* are (as you might guess based on their name) simpler. For a 
simple survey, you can define a `survey.json` file that describes the questions 
that should be asked. For example:

```json
{
  "instructions": "Fill out this survey and click the \"Complete\" button to download results.",
  "linear": {
    "description": "Please answer each of the questions.",
    "q": [{
      "id": "q3", 
      "text": "What is your GPA?", 
      "type": "number"
    }, {
      "id": "q4", 
      "text": "I have had an engineering internship.", 
      "type": "checkbox"
    }, {
      "id": "q5", 
      "text": "If yes to Q4, please describe your experience.", 
      "type": "longResponse"
    }]
  }
}
```

To make the survey, save the JSON above as `simple-survey-1.json` or download
it from the [examples](#TODO). Continue on to [Generate Survey Links](./05-generate-survey-links.md)
to learn how to generate shareable links to surveys.


## Matrix Surveys

*Matrix surveys* allow you to ask tabulated or matrix-style questions. Their
JSON files are more complex and the survey results are much larger.

Matrix surveys require a `matrix` field added to the JSON. The matrix has an
optional `description` field and must have an `x` and `y` section defined to 
describe the X- and Y-axes of the matrix.

See the [Survey Examples](#TODO) for an example JSON file.


## Peer Surveys

*Peer surveys* are like matrix surveys, except they generate the X-axis of 
the matrix (the columns) from team information in a roster file. These are useful
for distributing unique surveys to each team to collect peer evaluations.
