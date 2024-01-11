# OSPAR: A Corpus for Extraction of Organic Synthesis Procedures with Argument Roles

This repository contains data for the JCIM paper: [OSPAR: A Corpus for Extraction of Organic Synthesis Procedure with Argument Roles](https://pubs.acs.org/doi/10.1021/acs.jcim.3c01449).

## OSPAR corpus

### Requirements
1. beautifulsoup4

### Download corpus
1. `git clone https://github.com/mlmachi/OSPAR`
2. `cd OSPAR`
3. `bash script.sh`

### Data directory
There are two versions of data.
`data_original` is the original data used in our work.
We also provide another version of data `data_revised_2023-06-29` because we find the change of the html version of *Organic Syntheses* which is used to create `.txt` files.

```
├── data_original
│   ├── OSPAR
│   └── OSPAR_synthesis_text_only
└── data_revised_2023-06-29
    ├── OSPAR
    └── OSPAR_synthesis_text_only
```

`OSPAR`
- contains B_WORKUP in `.ann`
- contains the full text of procedure including the work-up process.

`OSPAR_synthesis_text_only`
- does not contain B_WORKUP in `.ann`
- contains only the text of the synthesis part that excludes the work-up process.

## Rolesets
The rolesets used in OSPAR are provided in `rolesets.tsv`.

## Contact
If you have any questions and suggestions, please create an issue or email to [machi@eis.hokudai.ac.jp](mailto:machi@eis.hokudai.ac.jp).
