---
title: "Visualize Skyline participants daily survey responses behaviour"
output:
  html_document:
    df_print: paged
    
---

library(tidyverse)
library(lubridate)



###########################################################
# Get performance for skyline survey completion

###########################################################

### read filename from Qualtrics generated csv files


day_filepath =  "~/Documents/STUDY/EEG-Tobacco/DATA/SURVEYS/Day/"

evening_filepath = "~/Documents/STUDY/EEG-Tobacco/DATA/SURVEYS/Evening"

eff_evening_filepath = "~/Documents/STUDY/EEG-Tobacco/DATA/SURVEYS/Every3days"

cond_file = "~/Documents/STUDY/EEG-Tobacco/DATA/expe_condition.csv"


output_filepath = "~/Documents/STUDY/EEG-Tobacco/DATA/SURVEYS"

output_file = file.path(output_filepath, "behav_end_data.csv")



#### read qualtrics data sheet


# daily survey eff ctr messages

files_day <-dir(path= day_filepath, pattern = "*.csv") 

data_day <- files_day %>% 
  map(~ read_csv(file.path(day_filepath, .))) %>%
  reduce(bind_rows)


# daily evening survey
files_eve <-dir(path= evening_filepath, pattern = "*.csv") 

data_eve <-read.csv(file.path(evening_filepath, files_eve), header = TRUE, sep = ",", dec = ".")
as_tibble(data_eve)

# every 3 days evening survey
  
files_eff_eve <-dir(path= eff_evening_filepath, pattern = "*.csv") 

data_eff <-read.csv(file.path(eff_evening_filepath, files_eff_eve), header = TRUE, sep = ",", dec = ".")
as_tibble(data_eff)
    
  

#### rename columns and filter to get only completed surveys

data_day <-rename(data_day, date=EndDate, completed=Finished, ID = Q1, score =SC0)


data_eve <-rename(data_eve, date=EndDate, completed=Finished, ID = Q1)

data_eff <-rename(data_eff, date=EndDate, completed=Finished, ID = Q1)


#filter to get only the completed = True

data_day<-data_day %>%filter(completed == 'True')
data_eve<-data_eve %>%filter(completed == 'True')
data_eff<-data_eff %>%filter(completed == 'True')


#sort data by subject and count how many lines
data_tmp<- data_day %>%
  group_by(ID) %>%
  tally()
data_tmp <- rename(data_tmp, day_msg = n)


data_eve_tmp<- data_eve %>%
  group_by(ID) %>%
  tally()

data_eve_tmp <- rename(data_eve_tmp, eve_msg = n)

data_eff_tmp<- data_eff %>%
  group_by(ID) %>%
  tally()
  
data_eff_tmp <- rename(data_eff_tmp, ev3days = n)



#### create new dataset collating data for all surveys

sum_data<-left_join(data_tmp,data_eve_tmp, by = 'ID', copy=TRUE)
sum_data<-left_join(sum_data, data_eff_tmp, by = 'ID', copy=TRUE)

## add information from condition file

cond <- read_csv(cond_file)
as_tibble(cond)
cond <-rename(cond, ID = "Subject ID", condition = "Condition = Intervention")
cond$ID<-as.character(cond$ID)

sum_data<-left_join(sum_data, cond, by = 'ID', copy=TRUE)


# check number of pp doing the task
sum(sum_data$day_msg %in% 41:66)
sum(sum_data$day_msg <40)

mid_pp <- subset(sum_data, sum_data$day_msg %in% 0:40 )
sum(mid_pp$condition == 0, na.rm=TRUE)


#### create new dataset with pp cinpliant for daily messages


good_pp <-filter(sum_data, sum_data$day_msg>66)

good_pp<-good_pp %>% replace_na(list(Finished = 0, REMOVED = 0))

test<-good_pp %>% summarise_all(., funs(if(is.numeric(.)) sum(.) else "Total"))


sum(good_pp$eve_msg>22)

sum(good_pp$condition)


#### export to csv file

# export to csv
write_csv(good_pp, file.path(output_filepath, 'good_pp.csv') )




