# Spectra

An organizational data engineering and analytics tool suite.

- `doc` - Documentation
- `src` - Source code
    - `spectra` - The Spectra Python module
        - `core`
        - `cli`
        - `analytics`
    - `spectra-docs` - The source code for the docs site.


## Mac Setup

```
pip install rich numpy matplotlib pandas
brew install pandoc
brew install basictex
pip install -e .
```

## TODO

[] Spectra transform survey -in survey_id -o pdf 
[] spectra analyze --analyzer=attendance-flags --opts 
[] Spectra index surveys -in survey_id —elastic-info
[] Raw Data Capture
    [] Spectra new data —raw -t zoom-report -s section -in sourceDir
[] Attendance Ingesters
    [] Zoom: Spectra ingest zoom-reports -s section
    [] UCFHere: Spectra ingest zoom-reports -s section