# Make a Section


**Sections** represent a section of an organization. In academia, this 
is commonly a course section (hence the terminology), but this could
also be a team, team of teams, or business unit.

Spectra uses course roster files exported from Canvas LMS to generate sections.
If you don't use Canvas, that's okay. The roster file is simply a CSV file with
the following format:

| 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|:--|:--|:--|:--|:--|:--|:--|
| Name | Canvas User ID | User ID | NID | Sections | Team Name | Team ID | 

- **Name** - This is a comma-separated name in the form `Last, First Middle`. 
- **Canvas User ID** - The user ID from Canvas. This is a string and is used as
a unique identifier for the person. If you're making your own CSV file, this could
be an employee ID.
- **User ID** - This is ignored by Spectra.
- **NID** or **Network ID** - This is ignored by Spectra.
- **Sections** - This is ignored by Spectra.
- **Team Name** - This string is the human readable team name.
- **Group ID** - This is the Canvas group ID for the team. It is a string and is
used by Spectra as the unique identified of the group.



To make a new section, run:

```
spectra new section -r <path/to/your/roster.csv> --name <section-name>
```

Replace `<path/to/your/roster.csv>` with the path to your roster file and 
replace `<section-name>` with a section name of your choice. The section name
must be a valid directory name.