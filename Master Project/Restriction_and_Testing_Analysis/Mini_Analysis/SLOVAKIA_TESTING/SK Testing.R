#libraries
library(stringr)
library(tidyr)
library(dplyr)
library(rpart)
library(randomForest)
library(openair)
library(lubridate)
library(party)
library(ggplot2)
library(stringi)


#Reading data
testing.df <- read.csv("SLOVAKIA TESTING.csv",fileEncoding = "UTF-8-BOM")
testing.df


#Separating columns
testing1.df <- testing.df %>%
  separate(X.Date...Region...District...District_code...Gender...AgeGroup...PCR_Pos...PCR_Neg...PCR_Total.,sep=";",c("Date","Region","District","DistrictCode","Gender","AgeGroup","PCRPos","PCRNeg","PCRTotal"))

#Creating age categories
testing1.df[testing1.df == "\"00\""] <- 1
testing1.df[testing1.df == "\"01-04\""] <- 1
testing1.df[testing1.df == "\"05-09\""] <- 1
testing1.df[testing1.df == "\"10-14\""] <- 1
testing1.df[testing1.df == "\"15-19\""] <- 1
testing1.df[testing1.df == "\"20-24\""] <- 2
testing1.df[testing1.df == "\"25-34\""] <- 2
testing1.df[testing1.df == "\"35-44\""] <- 3
testing1.df[testing1.df == "\"45-54\""] <- 3
testing1.df[testing1.df == "\"55-64\""] <- 4
testing1.df[testing1.df == "\"65_v\""] <- 4
testing1.df[testing1.df == "\"neznáme\""] <- 4
testing1.df[testing1.df == "\"999\""] <- 4

#Creating categories where Pos is bigger or smaller than Neg
testing2.df <- testing1.df %>%
  mutate(Status = case_when(
    PCRPos > PCRNeg ~ "1",
    PCRPos < PCRNeg ~ "2"
  ))
testing2.df



#Removing NA values
testing2.df$Status[is.na(testing2.df$Status)] <-0
testing2.df <- subset(testing2.df,Gender != "NA")

testing2.df


#CHanging data types
testing2.df$Date <- as.Date(testing2.df$Date)
testing2.df$AgeGroup <- as.numeric(testing2.df$AgeGroup)
testing2.df$PCRPos <- as.numeric(testing2.df$PCRPos)
testing2.df$PCRNeg <- as.numeric(testing2.df$PCRNeg)
testing2.df$PCRTotal <- as.numeric(testing2.df$PCRTotal)
testing2.df$Status <- as.numeric(testing2.df$Status)
testing2.df$Gender <- as.factor(testing2.df$Gender)
testing2.df$Status <- as.factor(testing2.df$Status)

testing2.df
class(testing2.df)


#Filtering data by date
testing_final1.df <- testing2.df[testing2.df$Date > "2021-01-01" & testing2.df$Date < "2021-12-01",]
testing_final1.df

#Creating Random Forest Model
model1 <- ctree(Status ~ Gender + AgeGroup, data=testing_final1.df)
plot(model1)
#Saving the plot
jpeg('plot1.jpg',width=1000)


testing_final2.df <- testing1.df

#Changing to ASCII
testing_final2.df$Region <- stri_trans_general(testing_final2.df$Region, "Latin-ASCII")
testing_final2.df$District <- stri_trans_general(testing_final2.df$District, "Latin-ASCII")
testing_final2.df$AgeGroup <- stri_trans_general(testing_final2.df$AgeGroup,"Latin-ASCII")


testing_final2.df

#CHanging the age categories again
testing_final2.df[testing_final2.df == "\"00\""] <- "0-1"
testing_final2.df[testing_final2.df == "\"01-04\""] <- "1-4"
testing_final2.df[testing_final2.df == "\"05-09\""] <-"5-9"
testing_final2.df[testing_final2.df == "\"10-14\""] <- "10-14"
testing_final2.df[testing_final2.df == "\"15-19\""] <- "15-19"
testing_final2.df[testing_final2.df == "\"20-24\""] <- "20-24"
testing_final2.df[testing_final2.df == "\"25-34\""] <- "25-34"
testing_final2.df[testing_final2.df == "\"35-44\""] <- "35-44"
testing_final2.df[testing_final2.df == "\"45-54\""] <- "45-54"
testing_final2.df[testing_final2.df == "\"55-64\""] <- "55-64"
testing_final2.df[testing_final2.df == "\"65_v\""] <- "65-99"
testing_final2.df[testing_final2.df == "\"nezname\""] <- "unknown"
testing_final2.df[testing_final2.df == "\"999\""] <- "99-more"

#Writing the csv
write.csv(testing_final2.df,"SlovakiaTesting.csv")

#Saving to mongo
g=mongo(collection="publictransport",url="mongodb://127.0.0.1:27017/SlovakiaTesting")
g$insert(testing_final2.df)
```