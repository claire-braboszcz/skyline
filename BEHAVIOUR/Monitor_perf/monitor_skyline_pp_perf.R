---
title: "Visualize Skyline participants daily survey responses behaviour"
output:
  html_document:
    df_print: paged
    
---

library(tidyverse)
library(lubridate)
library(here)


###########################################################
# Get performance for skyline survey completion

###########################################################

### read filename from Qualtrics generated csv files


day_filepath =  here::here("Day")

evening_filepath = here::here("Evening")

eff_evening_filepath = here::here("Every3days")



output_file = file.path(here::here(), paste(today(),"monitoring.csv"))


filename_current = file.path(here::here(), "current_pps.csv")


filename_phone = "/home/claire/Documents/STUDY/EEG-Tobacco/DATA/current_phone.csv"




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
    
  


#### read current participants list and get date in right format

d_pps<-read.csv(filename_current, header = TRUE, sep = ",", dec = ".")
as_tibble(d_pps)
d_pps$ID<-factor(d_pps$ID)

# put dates in right format
d_pps$START <-dmy(d_pps$START)



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




#### create new dataset including the information about the start date and add evening info

sum_data<-right_join(data_tmp, d_pps, by = 'ID', copy=TRUE) # join the two dataset, keep all values from current pps

sum_data<-left_join(sum_data, data_eve_tmp, by = 'ID', copy=TRUE)

sum_data<-left_join(sum_data, data_eff_tmp, by = 'ID', copy=TRUE)




# reposition start date column to be second position

sum_data<- sum_data %>% select(ID, START, everything())



# arrange in descending START time order

sum_data<- sum_data %>% arrange(desc(START))



# get how long the pp has been doing the experiment

sum_data$run_for <- today()-sum_data$START

#### check day performances


# add column for expected number of daily messages completed
sum_data$day_msg_exp<-3*(sum_data$run_for)

#### add column for expected number of evening messages completed

sum_data$eve_msg_exp<-1*(sum_data$run_for)



#### column for diff expected -n 


sum_data$day_diff_exp_real <- sum_data$day_msg_exp-sum_data$day_msg


sum_data$eve_diff_exp_real <- sum_data$eve_msg_exp-sum_data$eve_msg



#### Get the last date pps completed a day survey


data_day$date<- as_date(data_day$date)
data_day$date <-ymd(data_day$date)

test<- select(data_day, ID, date)

# remove first two rows
test <-test[-c(1:2),]

test$date <- as_date(test$date)

most_recent<-test %>% 
  group_by(ID) %>%
  slice(which.max(as.Date(date, '%m/%d/%Y')))
  

sum_data<-left_join(sum_data, most_recent, by = 'ID', copy=TRUE)




#### read current phone number and add column to dataset

d_phone<-read.csv(filename_phone, header = TRUE, sep = ",", dec = ".")
as_tibble(d_phone)
d_phone$ID<-factor(d_phone$ID)

sum_data<-left_join(sum_data, d_phone, by = 'ID', copy=TRUE)

sum_data <- rename(sum_data, most_recent = date)


#### arrange in descending day message completed

sum_data<- sum_data %>% arrange(desc(day_diff_exp_real))



#### export to csv file

# export to csv
write_csv(sum_data, output_file)


#################################################################

# Get performance for pp who finished the study

#################################################################


followup_filepath = "~/Documents/STUDY/EEG-Tobacco/DATA/SURVEYS/FollowUp"

output_file_followup = file.path(output_filepath, paste(today(),"end_of_study.csv"))


# read follow up data
files_followup <-dir(path= followup_filepath, pattern = "*.csv") 

data_followup <-read.csv(file.path(followup_filepath, files_followup), header = TRUE, sep = ",", dec = ".")
as_tibble(data_followup)


# rename columns of interest and filter to get only the completed = True
data_followup <-rename(data_followup, date=RecordedDate, completed=Finished, ID = Q1, Interview=Q81)
data_followup$ID<-factor(data_followup$ID)

# select only columns of interest
data_followup<-data_followup %>% select(date, completed, ID, Interview)

data_followup<-data_followup %>%filter(completed == 'True')

# copy of sum_data
end_data <- sum_data

# drop columns

end_data<-inner_join(end_data, data_followup, by = 'ID', copy=TRUE)

end_data <- select(end_data, -starts_with("X."))

end_data$day_msg_perf <- end_data$day_msg - ((3*28)- (3*28*20/100)) 
end_data$eve_msg_perf <- end_data$eve_msg - (28- (28*20/100)) 
end_data$every3day_msg_perf <- end_data$ev3days - ((3*28)- (3*28*20/100)) 


# export to csv
write_csv(end_data, output_file_followup)








