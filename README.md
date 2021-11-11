<h2 align="center"> BMSCE Question Paper Ripper </h2>
<p align="center">
  <strong>
  Rip previous year question papers from the e-library automatically in seconds.
  </strong>
  <br>
  Saves around 7+5*(3*15) = 232 clicks on average when trying to download the last 5 years papers for a particular subject of a branch.
</p>

### New in V1.2

-  Makes it easier to find courses that have moved up or down a semester by ripping papers and storing with the entire course name. 

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

1. Clone the repo `git clone https://github.com/shaansubbaiah/bmsce-paper-ripper.git`
1. Run `pip install -r requirements.txt`
1. Download chromedriver from https://chromedriver.chromium.org/downloads
1. Extract it and put it in the /bmsce-paper-ripper directory
1. Set the COURSE, BRANCH, SEMESTER, etc values in `ripper.py`
1. Run `python ripper.py`

## Config

```
LIBRARY_URL     = (String), e-library url
USERNAME        = (String), e-library username
PASSWORD        = (String), e-library password
SEMESTER        = (String), valid semester list below
BRANCH          = (String), valid branches list below
COURSE          = (String), eg.'TFC' for 16CS6DCTFC.pdf, leave empty to to rip papers for every course
LAST_N_YEARS    = (Number), n years papers to rip, ideally 1-5
LONG_FILE_NAMES = (Bool),   Enable to include the entire course name in the files and folder (Ture/False)
```

```
### Valid branch parameters:
# ARCHITECTURE
# BIOTECHNOLOGY
# CHEMICAL ENGINEERING
# CIVIL ENGINEERING
# COMPUTER SCIENCE
# INFORMATION SCIENCE
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
Opening SIXTH SEMESTER
Opening COMPUTER SCIENCE AND INFORMATION SCIENCE
·· Adding 2020-21_GRADE_IMPROVEMENT Papers
   ·· pages found: 1
·· Adding 2019-20_SUPPLEMENTARY Papers
   ·· pages found: 1, 2 
·· Adding 2018-19_SUPPLEMENTARY Papers
   ·· pages found: 1, 2 
·· Adding 2018-19_SEMESTER_MAKE_UP Papers
   ·· pages found: 1
·· Adding 2018-19_MAIN_EXAMINATION Papers
   ·· pages found: 1, 2 
Using Extracted Cookie  C4A5AE44D547F542A0CA8C25DFXXXXXX
Extracting PUBLIC LINKS
   ·· took 0.430s
Exporting CSV
Downloading PDFs
   ·· took 5.091s
💀 Ripped 58 files.         
Took 13.201s.
```

Example folder structure generated

```
RIPPED_PAPERS
├── 16CS6DCGCT_Green_Computing
│   └── 2018-19_SUPPLEMENTARY_Green_Computing_16CS6DCGCT.pdf
├── 16CS6DCHSHS1_Software_Project_Management_and_Finance
│   └── 2018-19_SUPPLEMENTARY_Software_Project_Management_and_Finance_16CS6DCHSHS1.pdf
├── 16CS6DCMAD_Mobile_Application_Development
│   ├── 2019-20_SUPPLEMENTARY_Mobile_Application_Development_16CS6DCMAD.pdf
│   └── 2020-21_GRADE_IMPROVEMENT_Mobile_Application_Development_16CS6DCMAD.pdf
├── 16CS6DCMAD_Mobile_Applications_Development
│   ├── 2018-19_MAIN_EXAMINATION_Mobile_Applications_Development_16CS6DCMAD.pdf
│   ├── 2018-19_SEMESTER_MAKE_UP_Mobile_Applications_Development_16CS6DCMAD.pdf
│   └── 2018-19_SUPPLEMENTARY_Mobile_Applications_Development_16CS6DCMAD.pdf
├── 16CS6DCOOM_Object_Oriented_Modeling_and_Design
│   ├── 2018-19_MAIN_EXAMINATION_Object_Oriented_Modeling_and_Design_16CS6DCOOM.pdf
│   ├── 2018-19_SEMESTER_MAKE_UP_Object_Oriented_Modeling_and_Design_16CS6DCOOM.pdf
│   └── 2018-19_SUPPLEMENTARY_Object_Oriented_Modeling_and_Design_16CS6DCOOM.pdf
├── 16CS6DCOOM_Object_Oriented_Modelling_and_Design
│   └── 2019-20_SUPPLEMENTARY_Object_Oriented_Modelling_and_Design_16CS6DCOOM.pdf
├── 16CS6DCTFC_Theoretical_Foundations_of_Computations
│   ├── 2018-19_MAIN_EXAMINATION_Theoretical_Foundations_of_Computations_16CS6DCTFC.pdf
│   ├── 2018-19_SUPPLEMENTARY_Theoretical_Foundations_of_Computations_16CS6DCTFC.pdf
│   └── 2019-20_SUPPLEMENTARY_Theoretical_Foundations_of_Computations_16CS6DCTFC.pdf
├── 16CS6DEAIN_Artificial_Intellience
│   └── 2019-20_SUPPLEMENTARY_Artificial_Intellience_16CS6DEAIN.pdf
├── 16CS6DEAIN_Artificial_Intelligence
│   ├── 2018-19_MAIN_EXAMINATION_Artificial_Intelligence_16CS6DEAIN.pdf
│   └── 2018-19_SUPPLEMENTARY_Artificial_Intelligence_16CS6DEAIN.pdf
├── 16CS6DECCT_Cloud_Computing
│   ├── 2018-19_MAIN_EXAMINATION_Cloud_Computing_16CS6DECCT.pdf
│   ├── 2018-19_SUPPLEMENTARY_Cloud_Computing_16CS6DECCT.pdf
│   ├── 2019-20_SUPPLEMENTARY_Cloud_Computing_16CS6DECCT.pdf
│   └── 2020-21_GRADE_IMPROVEMENT_Cloud_Computing_16CS6DECCT.pdf
├── 16CS6DECNS_Cryptography_and_Network_Security
│   ├── 2018-19_MAIN_EXAMINATION_Cryptography_and_Network_Security_16CS6DECNS.pdf
│   ├── 2018-19_SUPPLEMENTARY_Cryptography_and_Network_Security_16CS6DECNS.pdf
│   └── 2019-20_SUPPLEMENTARY_Cryptography_and_Network_Security_16CS6DECNS.pdf
├── 16CS6DEFLN_Fuzzy_Logic_and_Neural_Networks
│   ├── 2018-19_MAIN_EXAMINATION_Fuzzy_Logic_and_Neural_Networks_16CS6DEFLN.pdf
│   ├── 2018-19_SUPPLEMENTARY_Fuzzy_Logic_and_Neural_Networks_16CS6DEFLN.pdf
│   └── 2019-20_SUPPLEMENTARY_Fuzzy_Logic_and_Neural_Networks_16CS6DEFLN.pdf
├── 16CS6HSHS1_Software_Project_Management_and_Finance
│   ├── 2018-19_MAIN_EXAMINATION_Software_Project_Management_and_Finance_16CS6HSHS1.pdf
│   ├── 2019-20_SUPPLEMENTARY_Software_Project_Management_and_Finance_16CS6HSHS1.pdf
│   └── 2020-21_GRADE_IMPROVEMENT_Software_Project_Management_and_Finance_16CS6HSHS1.pdf
├── 16IS6DCCDN_C#_and_NET
│   └── 2020-21_GRADE_IMPROVEMENT_C#_and_NET_16IS6DCCDN.pdf
├── 16IS6DCCDN_C_and_NET
│   └── 2019-20_SUPPLEMENTARY_C_and_NET_16IS6DCCDN.pdf
├── 16IS6DCCDN_C_hash_and_NET
│   └── 2018-19_MAIN_EXAMINATION_C_hash_and_NET_16IS6DCCDN.pdf
├── 16IS6DCCDN_C_Hash_and_Net
│   └── 2018-19_SUPPLEMENTARY_C_Hash_and_Net_16IS6DCCDN.pdf
├── 16IS6DCCNS_Computer_Networks_and_Security
│   ├── 2018-19_MAIN_EXAMINATION_Computer_Networks_and_Security_16IS6DCCNS.pdf
│   ├── 2018-19_SUPPLEMENTARY_Computer_Networks_and_Security_16IS6DCCNS.pdf
│   ├── 2019-20_SUPPLEMENTARY_Computer_Networks_and_Security_16IS6DCCNS.pdf
│   └── 2020-21_GRADE_IMPROVEMENT_Computer_Networks_and_Security_16IS6DCCNS.pdf
├── 16IS6DCEAM_Entrepreneurship_and_Management
│   ├── 2018-19_MAIN_EXAMINATION_Entrepreneurship_and_Management_16IS6DCEAM.pdf
│   ├── 2019-20_SUPPLEMENTARY_Entrepreneurship_and_Management_16IS6DCEAM.pdf
│   └── 2020-21_GRADE_IMPROVEMENT_Entrepreneurship_and_Management_16IS6DCEAM.pdf
├── 16IS6DCSEO_Software_Engineering_and_Object_Oriented_Design
│   ├── 2018-19_MAIN_EXAMINATION_Software_Engineering_and_Object_Oriented_Design_16IS6DCSEO.pdf
│   ├── 2018-19_SUPPLEMENTARY_Software_Engineering_and_Object_Oriented_Design_16IS6DCSEO.pdf
│   ├── 2019-20_SUPPLEMENTARY_Software_Engineering_and_Object_Oriented_Design_16IS6DCSEO.pdf
│   └── 2020-21_GRADE_IMPROVEMENT_Software_Engineering_and_Object_Oriented_Design_16IS6DCSEO.pdf
├── 16IS6DCSNA_Social_Network_Analysis
│   ├── 2018-19_MAIN_EXAMINATION_Social_Network_Analysis_16IS6DCSNA.pdf
│   ├── 2018-19_SUPPLEMENTARY_Social_Network_Analysis_16IS6DCSNA.pdf
│   ├── 2019-20_SUPPLEMENTARY_Social_Network_Analysis_16IS6DCSNA.pdf
│   └── 2020-21_GRADE_IMPROVEMENT_Social_Network_Analysis_16IS6DCSNA.pdf
├── 16IS6DEMLG_Machine_Learning
│   ├── 2018-19_MAIN_EXAMINATION_Machine_Learning_16IS6DEMLG.pdf
│   ├── 2018-19_SUPPLEMENTARY_Machine_Learning_16IS6DEMLG.pdf
│   ├── 2019-20_SUPPLEMENTARY_Machine_Learning_16IS6DEMLG.pdf
│   └── 2020-21_GRADE_IMPROVEMENT_Machine_Learning_16IS6DEMLG.pdf
├── 16IS6DEPDC_Parallel_and_Distributed_Computations_Through_Java
│   └── 2018-19_SUPPLEMENTARY_Parallel_and_Distributed_Computations_Through_Java_16IS6DEPDC.pdf
├── _16IS6DEVCS_Virtualization_and_Cloud_Security
│   └── 2018-19_SUPPLEMENTARY_Virtualization_and_Cloud_Security__16IS6DEVCS.pdf
└── 16IS6DEVCS_Virtualization_and_Cloud_Security
    ├── 2018-19_MAIN_EXAMINATION_Virtualization_and_Cloud_Security_16IS6DEVCS.pdf
    ├── 2018-19_SUPPLEMENTARY_Virtualization_and_Cloud_Security_16IS6DEVCS.pdf
    └── 2019-20_SUPPLEMENTARY_Virtualization_and_Cloud_Security_16IS6DEVCS.pdf

25 directories, 58 files
```
