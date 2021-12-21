# Testing and Restrictions - Maria Migrova #

This part of the project is intended to analyse testing and different gouvernment restrictions in the world and also testing in Slovakia.
All data was collected on website Our Wolrd In Data: https://ourworldindata.org/coronavirus.

The data was downloaded directly from the website as a csv file and read in the R studio. After all the analysis the data was saved in MongoDB through RStudio.

These steps were performed: 
1. Downloading the csv file from the website
2. Reading the csv file in R Studio
3. Cleaning the data 
4. Analysing the data in R Studio and Python
5. Saving the data in MongoDB

These analysis were performed: 
1. SVM linear regression analysing the relationship between number of cases and different restrictions.
2. Dumbbell plot showing a difference in central Europe countries in stringency index between 1/1/2021 and 25/11/2021.
3. Comparing stringency index in Slovakia and Ireland by time.
4. Random forest model showing average prediction in Slovakia in cases if number of Positive PCR tests is bigger or smaller than number of Negative PCR tests by Age and Gender.
5. Barchart showing a difference in n. of positive PCR tests by gender and age group in Slovakia.
