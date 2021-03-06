#Loading Libraries
library(dplyr)
library(ggplot2)
library(e1071)
library(modelr)
library(Metrics)
library(plotly)
library(hrbrthemes)
library(processx)
library(mongolite)

#READING DATA
stringency.df <- read.csv("covid-stringency-index (3).csv",fileEncoding = "UTF-8-BOM")
masks.df <- read.csv("face-covering-policies-covid (1).csv",fileEncoding = "UTF-8-BOM")
stayhome.df <- read.csv("stay-at-home-covid (1).csv",fileEncoding = "UTF-8-BOM")
publicevents.df <- read.csv("public-events-covid (1).csv",fileEncoding = "UTF-8-BOM")
publictransport.df <- read.csv("public-transport-covid.csv",fileEncoding = "UTF-8-BOM")
schools.df <- read.csv("school-closures-covid (1).csv",fileEncoding = "UTF-8-BOM")
cases.df <- read.csv("owid-covid-data (2).csv",fileEncoding = "UTF-8-BOM")

#STAY HOME
#Changing data into date form
stayhome.df$Day <- as.Date(stayhome.df$Day)
#Filtering date
stayhome1.df <- stayhome.df[stayhome.df$Day > "2020-12-31" & stayhome.df$Day < "2021-12-07",]
stayhome1.df <- stayhome1.df %>%
  #Renaming
  rename(country = Entity, isocode = Code, Date = Day)%>%
  select(isocode, country, Date, stay_home_requirements)%>%
  #Grouping
  group_by(isocode,country)%>%
  #SUmmarising
  summarise(MaxStayHome = max(stay_home_requirements),
            MeanStayHome = mean(stay_home_requirements))

stayhome1.df

#STRINGENCY INDEX
#Changing data into date format
stringency.df$Day <- as.Date(stringency.df$Day)
#Filtering data
stringency1.df <- stringency.df[stringency.df$Day > "2020-12-31" & stringency.df$Day < "2021-12-07",]
stringency1.df <- stringency1.df %>%
  #Renaming
  rename(country = Entity, isocode = Code, Date = Day)%>%
  select(isocode, country, Date, stringency_index)%>%
  #Grouping
  group_by(isocode,country)%>%
  #Summarising
  summarise(MaxStringency = max(stringency_index),
            MeanStringency = mean(stringency_index))
stringency1.df

#MASKS
#Changing data into date format
masks.df$Day <- as.Date(masks.df$Day)
#Filtering date
masks1.df <- masks.df[masks.df$Day > "2020-12-31" & masks.df$Day < "2021-12-07",]
masks1.df <- masks1.df %>%
  rename(country = Entity, isocode = Code, Date = Day)%>%
  #Selecting
  select(isocode, country, Date, facial_coverings)%>%
  #Grouping
  group_by(isocode,country)%>%
  #Summarising
  summarise(MaxFacialCoverings = max(facial_coverings),
            MeanFacialCoverings = mean(facial_coverings))

masks1.df

#PUBLIC EVENTS
#CHanging data into date format
publicevents.df$Day <- as.Date(publicevents.df$Day)
#Filtering
publicevents1.df <- publicevents.df[publicevents.df$Day > "2020-12-31" & publicevents.df$Day < "2021-12-07",]
publicevents1.df <- publicevents1.df %>%
  rename(country = Entity, isocode = Code, Date = Day)%>%
  #Selecting
  select(isocode, country, Date,cancel_public_events)%>%
  #Grouping
  group_by(isocode,country)%>%
  #Summarising
  summarise(MaxCancelPublicEvents = max(cancel_public_events),
            MeanCancelPublicEvents = mean(cancel_public_events))

publicevents1.df

#PUBLIC TRANSPORT
#Changing data into date format
publictransport.df$Day <- as.Date(publictransport.df$Day)
#Filtering date
publictransport1.df <- publictransport.df[publictransport.df$Day > "2020-12-31" & publictransport.df$Day < "2021-12-07",]
publictransport1.df <- publictransport.df %>%
  rename(country = Entity, isocode = Code, Date = Day)%>%
  #Selecting columns
  select(isocode, country, Date, close_public_transport)%>%
  #Grouping
  group_by(isocode,country)%>%
  #Summarising
  summarise(MaxClosePublicTransport = max(close_public_transport),
            MeanClosePublicTransport = mean(close_public_transport))

publictransport1.df

#SCHOOLS
#Changing data into date format
schools.df$Day <- as.Date(schools.df$Day)
#Filtering
schools1.df <- schools.df[schools.df$Day > "2020-12-31" & schools.df$Day < "2021-12-07",]
schools1.df <- schools1.df %>%
  rename(country = Entity, isocode = Code, Date = Day)%>%
  #Selecting
  select(isocode, country, Date,school_closures)%>%
  #Grouping
  group_by(isocode,country)%>%
  #Summarising
  summarise(MaxSchoolClosure = max(school_closures),
            MeanSchoolClosure = mean(school_closures))

schools1.df

#CASES
#CHanging data into date format
cases.df$date <- as.Date(cases.df$date)
#Filtering
cases1.df <- cases.df[cases.df$date > "2020-12-31" & cases.df$date < "2021-12-07",]
cases1.df <- cases1.df %>%
  rename(country = location, isocode = iso_code, Date = date) %>%
  #Selecting columns
  select(isocode, country, Date, total_cases, new_cases)%>%
  #Grouping
  group_by(isocode,country)%>%
  #Summarising
  summarise(TotalCases = sum(new_cases),
            MaxCases = max(new_cases))

cases1.df

#Joining the data
home_stringency.df <- full_join(stayhome1.df,stringency1.df, by= c("isocode","country"))
home_stringency.df
home_stringency_masks.df <- full_join(home_stringency.df, masks1.df, by = c("isocode","country"))
home_stringency_masks.df
home_stringency_masks_publicevents.df <- full_join(home_stringency_masks.df, publicevents1.df, by = c("isocode","country"))
home_stringency_masks_publicevents.df
home_stringency_masks_publicevents_publictransport.df <- full_join(home_stringency_masks_publicevents.df, publictransport1.df, by = c("isocode","country"))
home_stringency_masks_publicevents_publictransport.df
home_stringency_masks_publicevents_publictransport_schools.df <- full_join(home_stringency_masks_publicevents_publictransport.df, schools1.df, by = c("isocode","country"))
home_stringency_masks_publicevents_publictransport_schools.df
final_dataset.df <- full_join(home_stringency_masks_publicevents_publictransport_schools.df, cases1.df, by = c("isocode","country"))
final_dataset.df

#There is 734 NA values in our dataset
sum(is.na(final_dataset.df))
#Removing the NA values
final_dataset1.df <- na.omit(final_dataset.df)
final_dataset1.df


#Creating the SVM model
modelsvm <- svm(TotalCases ~ MaxStayHome + MeanStayHome + MaxStringency + MeanStringency + MaxFacialCoverings +  MeanFacialCoverings +  MaxClosePublicTransport + MeanClosePublicTransport +MaxCancelPublicEvents + MeanCancelPublicEvents + MaxSchoolClosure + MeanSchoolClosure + MaxCases,data = final_dataset1.df)

#Adding predictions and residuals to the dataset
covid.svm <- final_dataset1.df %>%
  add_predictions(modelsvm)%>%
  add_residuals(modelsvm)

covid.svm

#Plotting the model
ggplot(covid.svm)+
  geom_line(aes(MaxStringency, pred), col = "red")+
  geom_line(aes(MaxStringency,TotalCases ))+
  labs(title="SVM model")

#Plotting the residuals
ggplot(covid.svm,aes(MaxStringency, resid))+
  geom_ref_line(h=0)+
  geom_line()+
  labs(title="Residuals of the SVM model")

#Splitting into train and test set
set.seed(1)
row.number <- sample(1:nrow(final_dataset1.df), 0.8*nrow(final_dataset1.df))
train = final_dataset1.df[row.number,]
test = final_dataset1.df[-row.number,]
dim(train)
dim(test)

#Adding predictions
train <- train %>%
  add_predictions(modelsvm)
test <- test %>%
  add_predictions(modelsvm)

#MAE, MSE, MAPE, RMSE
paste("MAE Train: ",round(mae(train$pred, train$TotalCases),2))
paste("MAE Test: ", round(mae(test$pred, test$TotalCases),2))
paste("MSE Train: ", round(mse(train$pred, train$TotalCases),2))
paste("MSE Test: ", round(mse(test$pred, test$TotalCases),2))
paste("MAPE Train: ", round(mape(train$pred, train$TotalCases),2))
paste("MAPE Test: ",round(mape(test$pred, test$TotalCases),2))
paste("RMSE Train: ",round(rmse(train$pred, train$TotalCases),2))
paste("RMSE Test: ",round(rmse(test$pred, test$TotalCases),2))


summary(final_dataset1.df$TotalCases)


#From these results we can see that there are some differences between some of the training and testing scores, mostly for MAPE and RMSE, which means that we could actually overfit the data. The MAPE (mean absolute percentage error) value is equal to 0.73 for training data and 0.65 for testing data. This MAPE score is excellent, and it is defined as actual to observed value minus the forecasted value.This means that our model’s predictions are, on average less than 1% off from the actual values.

#The MAE (mean absolute error) is equal to 435 814 for training set and 1 220 891 for testing set. It discribes the average forecasted distance from the true value. It might seem a little high, but our values ranges from 2 to 23 114 239, which means this value is not too bad. 

#The MSE (mean square error) refers to the mean of the squared difference between the predicted parameter and the observed parameter. The RMSE differes from MAE scores, which is telling us that there are probably many outlier residuals.

#RMSE means the squared value of the MSE. For example, for the training set the RMSE is equal 1 725 433 which means that models predicted actual value is around 1 725 433 units off. Which is not a bad number. 

#In general, this model did very well. 


stringency.df



#creating central Europe dataset
central_europe <- stringency.df %>%
  #Filtering by date
  filter(Day == "2021-01-01" | Day == "2021-11-15")%>%
  #Filtering by countries
  filter(Entity %in% c("Slovakia","Czechia", "Poland","Austria","Belgium","Luxembourg","Denmark","France","Germany","Hungary","Ireland","Liechtenstein","Netherlands","Switzerland","United Kingdom"))%>%
  rename(Country = Entity, Date = Day)
central_europe


#Paring the data
central_europe <- central_europe %>%
  mutate(paired = rep(1:(n()/2),each=2),
         Date=factor(Date),
         Country = factor(Country))

central_europe

#Plotting the data
central_europe %>% 
  ggplot(aes(x= stringency_index, y= reorder(Country,-stringency_index))) +
  geom_line(aes(group = paired))+
    geom_point(aes(color=Date), size=4) +
    theme(legend.position="top")+
  ggtitle("Change in Stringency index from 01/01/2021 to 15/11/2021")+
  theme_minimal()+
  theme(axis.title.y = element_blank(),
        axis.title.x = element_blank(),
        legend.title = element_blank())

#Saving the plot
ggsave("dumbbellplot.jpg",plot=last_plot())



#Saving data into mongo
a=mongo(collection="stringency",url="mongodb://127.0.0.1:27017/stringency")
a$insert(stringency1.df)

b=mongo(collection="masks",url="mongodb://127.0.0.1:27017/masks")
b$insert(masks1.df)

c=mongo(collection="stayhome",url="mongodb://127.0.0.1:27017/stayhome")
c$insert(stayhome1.df)

d=mongo(collection="publicevents",url="mongodb://127.0.0.1:27017/publicevents")
d$insert(publicevents1.df)

e=mongo(collection="publictransport",url="mongodb://127.0.0.1:27017/publictransport")
e$insert(publictransport1.df)

f=mongo(collection="schools",url="mongodb://127.0.0.1:27017/schools")
f$insert(schools1.df)

