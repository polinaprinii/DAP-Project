```{r}
library(tidyr)
library(dplyr)


testing.df <- read.csv("testing data.csv",fileEncoding = "UTF-8-BOM")


testing.df


testing1.df <- testing.df %>%
  select(iso_code,location,date,total_tests)%>%
  rename(isocode = iso_code, country = location)
testing1.df


testing1.df$date <- as.Date(testing1.df$date)

testing_final.df <- testing1.df[testing1.df$date > "2020-12-31" & testing1.df$date < "2021-11-24",]
testing_final.df



testing_final1.df <- aggregate(testing_final.df$total_tests, list(testing_final.df$country),FUN=sum,na.rm=TRUE)
testing_final1.df <- testing_final1.df%>%
  rename(country = Group.1,
         tests = x)
testing_final1.df

ISO <- testing_final.df %>%
  select(isocode,country)%>%
  distinct(isocode,country)

ISO

testing_final1.df <- right_join(ISO,testing_final1.df, by= c("country"))
testing_final1.df

write.csv(testing_final1.df,"testing.csv")


z=mongo(collection="testing",url="mongodb://127.0.0.1:27017/testing")
z$insert(testing_final1.df)