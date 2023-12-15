# CodeUP Anomaly Detection Analysis

## Project Overview
This project focuses on answering questions that a superior might have on a particular data set, while exploring anomaly detection.

## Goals
- To explore the dataset and understand the factors that can answer the questions.
- To visualize the findings that help answer the questions.
- To find additional information that can be of helpful.

## Initial Questions
5. At some point in 2019, the ability for students and alumni to access both curriculums (web dev to ds, ds to web dev) should have been shut off. Do you see any evidence of that happening? Did it happen before?
6. What topics are grads continuing to reference after graduation and into their jobs (for each program)?
7. Which lessons are least accessed?
8. Anything else I should be aware of?

## Project Plan
1. Acquire
- get the data from CodeUP SQL server
- look at it
- describe, info, head, shape
- understand what the data means/is

2. Wrangle
- clean the data
- correct datatypes
- univariate analysis

3. Explore
- establish relationships using multivariate analysis
- visualize
- summarize


## Data Dictionary

| Feature       | Definition                                 |
|---------------|--------------------------------------------|
| date          | Date where a log or path occurs (index)    |
| time          | Time of the log                            |
| path          | Web address                                |
| user_id       | Personal identification number for a single student or staff |
| cohort_id     | Identification number for a particular cohort|
| ip            | Intermet address for the log               |
| cohort_name   | Name of the cohort                         |
| program_id    | Identification number for the program the student or staff is in |
| start_date    | Cohort start date                          |
| end_date      | Cohort end date                            |
| updated_at    | Last log from the user                     |


## Steps to Reproduce
1. Download this repository (wrgangle.py and project_anomaly_detection.ipynb).
2. Obtain access to codeup SQL server.
3. Run it

## Takeaways
- Curriculum Access Restriction in 2019
Pre-2019: Avg. daily path visits were 60.7
Post-2018: Avg. daily path visits dropped to 10.6
Impact: An 82.5% decrease in visits indicates effective restriction of cross-curriculum access.

- Post-Graduation Curriculum References
Web Dev Graduates:
index.html - 1011 times
javascript-i - 736 times
html-css - 542 times
Java Graduates:
javascript-i - 4229 times
spring - 3760 times
search/search_index.json - 3562 times
Data Science Graduates:
search/search_index.json - 493 times
sql/mysql-overview - 275 times
classification/overview - 266 times
The data reflects targeted access to specific topics, suggesting ongoing relevance to professional work.

- Cohort 28 ('Staff') is the only cohort with suspicious path usage, with 800 more unique path visits compared to all other cohorts.

- Low traffic paths
There are 467 paths that only were visited one time