# Generate Survey Links

Coming soon.


## Simple and Matrix Surveys

Once you have your survey JSON file saved as `survey.json`, you can run:

```bash
spectra mklink -s survey.json
```

This will output something like:

```
Generating link ...

https://surveyor-next.apps.triple.engineering/survey.html?data=dZKxTuQwEIZfZeR6hcSxNDTohHSIjjsKCrjCcf5srHU8Wc94sxHadz87S0Gko4tHnu%2F%2FxpMP46Noyk49RzF3ZH75EIizkvZeSHI6YiYbW3LBu32pgt7NAw9jgOLdUJNVOZIytTzFwLalBMlB5YpecjN4XXo%2Ba3T0ll7RPHBOArkyGzLBR9hUsj9MC3HJj1WmujwHWEFJlwmJYF1P3C24Q4YsygvhUC6%2FXbqXEZhr1bf1cLiu34qT1tMTdUCgYSaFHai3Qug6lPGPIMfDkKN3tpJp8lriciLbHr1wWpJ0HlE5qdyJO3Pe0HexP%2F4fu0ucRyovO3HaFwRNKO9dNOxi9G3IJ%2FXmK%2FW1t1pRc7V8fP55%2F7U55qFBWjVv10q9LTP3ZV82EuKubAGpGvmoSFF6P65sXA%2B3b%2Fi0Qt6ukB3NkPor%2FN5uaLws77LSBhdLnMYSguiwYgeOuz%2BQsSwU5vz3fP4H

Max URL length is 559
```

You can use the generated link to share your survey.

## Peer Surveys

Team surveys are a bit different because they rely on an organization roster
to autogenerate a unique link for each team for peer evaluations. Before
creating a peer survey, you must have [created a section](./03-make-a-section.md).

Once you have a section created and a survey JSON file (e.g. `peer-survey.json`) 
defined, you can run:

```bash
spectra mklink -s peer-survey.json --section .spectra-data/sections/YOUR-SECTION-ID
```
