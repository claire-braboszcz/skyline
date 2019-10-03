
You will need to have the R packages tidyverse and lubridate installed. 

You also need to change the filepaths at the top of the script to match your local configuration. 

!! the script sets today's date as a marker to compute the number of expected messages. 

The Qualtrics reports for each type of intervention, control, evening, every 3 days messages and follow up questionnaires need first to be downloaded then saved in the corresponding folder (Day/Evening/Every3days/FollowUp)


The script generates 2 .csv files:

1. the _monitoring.csv file contains:

- participant ID
- start date
- number of day time messages completed
- number of evening messages completed
- number of every 3 days evening messages completed
- number of days the study has run for a participant
- the expected number of day time message
- the expected number of evening message
- the difference between expected and real number of day time messages
- the difference between expected and real number of evening messages
- the most recent date when a message was completed

2. the _end_of_study.csv file contains:

- participant ID
- start date of the experiment
- number of day time messages completed
- number of evening messages completed
- number of every 3 days evening messages completed 
- how many days since the start of the experiment
- most recent date when a day survey has been completed
- name
- email
- phone of the pp
- if pp said yes to take part in the interview (!! you have to make sure they are in the intervention condition before giving their contact to Lily)
- day survey completion performance (NB survey completed - 80% of total of day surveys)  
- evening survey completion performance (NB survey completed - 80% of total of evening surveys)  
