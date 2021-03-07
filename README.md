<h2 align="center"> BMSCE Paper Ripper </h2>
<p align="center">
  <strong>
  Rip papers from the elibrary automatically in seconds.
  </strong>
  <br>
  Saves around `7+5*(3*15) = 232` clicks on average when trying to download the last 5 years papers for a particular subject of a branch.
  <br>
  Downloads the papers in PDF fromat to `/ripped_pds' folder and exports the links to CSV.
</p>

Output for default config (last 1 year's papers)

```
Starting Ripper
---> Opening SIXTH SEMESTER
---> Opening COMPUTER SCIENCE AND INFORMATION SCIENCE
---> Sourcing PDF links
------> Adding 2019_AND_2020_SUPPLEMENTARY_EXAMINATIONS Papers
---> Exporting CSV
---> Downloading PDFs
------> http://103.40.80.24/cdhome/221/379/390/1202/4043_img/16IS6DCSEO.pdf
------> http://103.40.80.24/cdhome/221/379/390/1202/4043_img/16CS6DCOOM.pdf
------> http://103.40.80.24/cdhome/221/379/390/1202/4043_img/16IS6DCSNA.pdf
------> http://103.40.80.24/cdhome/221/379/390/1202/4043_img/16IS6DEMLG.pdf
------> http://103.40.80.24/cdhome/221/379/390/1202/4043_img/16CS6DECNS.pdf
------> http://103.40.80.24/cdhome/221/379/390/1202/4043_img/16CS6DCTFC.pdf
------> http://103.40.80.24/cdhome/221/379/390/1202/4043_img/16CS6DEFLN.pdf
------> http://103.40.80.24/cdhome/221/379/390/1202/4043_img/16CS6DCMAD.pdf
------> http://103.40.80.24/cdhome/221/379/390/1202/4043_img/16CS6DEAIN.pdf
------> http://103.40.80.24/cdhome/221/379/390/1202/4043_img/16IS6DCCDN.pdf
Ripped. 💀
```

## Setup

- Clone the repo `git clone https://github.com/shaansubbaiah/bmsce-paper-ripper.git`
- Run `pip install -r requirements.txt`
- Set the branch, sem, etc in `ripper.py`
- Run `python ripper.py`

NOTE: In case you dont have the web driver for your browser in your PATH, get it here

`Chrome: https://sites.google.com/a/chromium.org/chromedriver/downloads`
`Firefox: https://github.com/mozilla/geckodriver/releases`

## Config

```
LIBRARY_URL  = e-library url (String)
USERNAME     = e-library username (String)
PASSWORD     = e-library password (String)
SEMESTER     = (String), valid semester list below
BRANCH       = (String), valid branches list below
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
