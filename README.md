<h2 align="center"> BMSCE Question Paper Ripper </h2>
<p align="center">
  <strong>
  Rip previous year question papers from the e-library automatically in seconds.
  </strong>
  <br>
  Saves around 7+5*(3*15) = 232 clicks on average when trying to download the last 5 years papers for a particular subject of a branch.
</p>

### New in V1.1

- Supports optionally ripping only a particular course's papers
- Supports parallel public link extraction and downloads

  Difference in speed when ripping last 5 years, 32 subjects, 148 pdf files

  | Version              | v1.0            | v1.1              |
  | -------------------- | --------------- | ----------------- |
  | Download Type        | Serial Download | Parallel Download |
  | Link Extraction Time | 10.377s         | 0.356s            |
  | Download Time        | 65.736s         | 0.327s            |
  | Overall Time         | 93.209s         | 18.171s           |

## Features

- Parallel downloads!
- Much faster than manually navigating, downloading from the site
- Download specifying the Course, Branch, Semester and last N years to retrieve papers
- Exports a list of public paper urls to CSV
- Renames the files with the exam type and year held
- Papers from different years of a particular subject are placed in a common folder

## Setup

- Clone the repo `git clone https://github.com/shaansubbaiah/bmsce-paper-ripper.git`
- Run `pip install -r requirements.txt`
- Download chromedriver from https://chromedriver.chromium.org/downloads
- Extract it and put it in the /bmsce-paper-ripper directory
- Set the COURSE, BRANCH, SEMESTER, etc values in `ripper.py`
- Run `python ripper.py`

## Config

```
LIBRARY_URL  = e-library url (String)
USERNAME     = e-library username (String)
PASSWORD     = e-library password (String)
SEMESTER     = (String), valid semester list below
BRANCH       = (String), valid branches list below
COURSE       = (String), eg.'TFC' for 16CS6DCTFC.pdf, leave empty to to rip papers for every course
LAST_N_YEARS = n years papers to rip (Integer), ideally 1-5
```

```
### Valid branch parameters:
# ARCHITECTURE
# BIOTECHNOLOGY
# CHEMICAL ENGINEERING
# CIVIL ENGINEERING
# COMPUTER SCIENCE AND INFORMATION SCIENCE
# ELECTRICAL AND ELECTRONIC ENGINEERING
# ELECTRONICS AND COMMUNICATION ENGINEERING
# INDUSTRIAL ENGINEERING AND MANAGEMENT
# INSTRUMENTATION ENGINEERING
# MECHANICAL ENGINEERING
# MEDICAL ELECTRONICS
# TELECOMMUNICATION ENGINEERING

### Valid semester parameters:
# FIRST SEMESTER
# SECOND SEMESTER
# THIRD SEMESTER
# FOURTH SEMESTER
# FIFTH SEMESTER
# SIXTH SEMESTER
# SEVENTH SEMESTER
# EIGHT SEMESTER

### UNSUPPORTED semester parameters:
# MATHEMATICS QUESTION PAPERS
# MBA QUESTION PAPERS
# MCA AUTONOMOUS QUESTION PAPERS
# MCA VTU Question Papers
# M.Tech QUESTION PAPERS
```

Example Terminal Output

```
Starting Ripper
---> Opening SIXTH SEMESTER
---> Opening COMPUTER SCIENCE AND INFORMATION SCIENCE
------> Adding 2019-20_SUPPLEMENTARY Papers
---------> page 1 2
------> Adding 2018-19_SUPPLEMENTARY Papers
---------> page 1 2
------> Adding 2018-19_SEMESTER_MAKE_UP Papers
---------> page 1
------> Adding 2018-19_MAIN_EXAMINATION Papers
---------> page 1 2
---> Extracting PUBLIC LINKS
------> Took 0.117s
---> Exporting CSV
---> Downloading PDFs
------> Took 0.134s
Ripped. 💀. Took 8.191s
```

Example folder structure generated

![output files pic](./assets/output_files_pic.png)
