
You will need to have the R packages tidyverse and lubridate installed. 

You also need to change the filepaths at the top of the script to match your local configuration. 

!! the script sets today's date as a marker to compute the number of expected messages. If you are checking performances later than the completion date you need to adjust for that

The generated document contains for each pp:
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

The Qualtrics reports for each type of intervention, control, evening and every 3 days messages need first to be downloaded then saved in the corresponding folder (Day/Evening/Every3days)
