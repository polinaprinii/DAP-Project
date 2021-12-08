# Database and Analytics Programming Project #

## *Project Aim:* ##

The project aims to perform analysis using the data collated by the individual work **outlined below** to estimate and report on a multiple regression model to facilitate the understanding of the criteria that dictates the Covid-19 mortality rates and useful for the prediction of the same.
Taking the following approach of programmatically combining the three individual CSV datasets via Python 3 in Jupyter Notebook and R Studio to allow for the construction of multiple linear regression analysis the project looks to conclude the finding in this report. (insert link to report) 

## *Individual Work:* ##

This area outlines the individual efforts to extract, clean and transform the datasets under analysis with the end goal of combining said datasets into one for Multiple Linear Regression.

### Total Vaccinations - Polina Prinii ###
The Total Vaccination dataset aims to look and identify the following totals:

- Total vaccines administered to the population for each country (inclusive of 2 dose protocols).
- Number of fully vaccinated individuals.
- Total boosters administered to the population.

The dataset in question looks at the following period of 01/01/2021 to 24/11/2021. With the aim to predict mortality rates for the upcoming year.

***Programmatic Approach:***

The following programmatic approach is used to extract, transform, load and analyse data in preparation for Multiple Linear Regression.<br />
Note all scripting is undertaken using the Python programming language, scripts can be found in the following [folder](https://github.com/polinaprinii/DAP-Project/tree/main/Vaccine_Analysis_by_Country).

**Step 1:** Environment setup in PyCharm to store all coding undertaken throughout the data ETL process.<br />
**Step 2:** Extract raw datasets from Git. <br />
**Step 3:** Import raw dataset to MongoDB.<br />
**Step 4:** Transform datasets in MongoDB.<br />
**Step 5:** Import datasets to PostgreSQL.<br />
**Step 6:** Assign relationships within tables in PostgreSQL.<br />
**Step 7:** Visualise data in meaningful ways.<br />
**Step 8:** Export final table aka dataset for groups efforts in CSV format. <br />

### Testing Dataset - Maria Migrova ###
The goal of this dataset is to summarise the number of tested people by each country in the world.

This dataset consists of: 
- isocode of each country
- country name
- tests = the total number of tests performed by each country in total from 01/01/2021 - 24/11/2021

***Programmatic Approach:***
Our dataset was loaded, cleaned and analysed using R Studio. 

These steps were undertaken:
1. Downloading the csv dataset from GitHub.
2. Reading the csv dataset in R Studio using read.csv() function and UTF-8-BOM file encoding.
3. Transforming the dataset into Json Format (WILL BE DONE)
4. Importing RAW dataset to MongoDB (WILL BE DONE)
5. Extracting the dataset from MongoDB as a csv file
6. Reading the csv file in R Studio again.
7. Aggregating the dataset using aggregate() function to get a summary of all tests performed by each country.
8. Analysing and visualising the data.
9. Writing the final dataset into a csv file which will be later used for the multiple linear regression.


### Restrictions Dataset - Maria Migrova ###
This dataset consists of a data about different restriction level in each country.

The dataset consists of: 
- isocode of each country
- country name
- MaxStringencyIndex - This is the maximal stringency index for each country which ranges from 0 - 100 (strictest). It is based on nine response indicators including school closures, workplace closures and travel bans.
- MeanStringencyIndex - This is the average stringency index for each country from 01/01/2021 - 24/11/2021
- MaxFacialCoverings - This is the maximal facial coverings restriction level for each country. It ranges from 0 - 4 (strictest). NA - No data, 0- No policy, 1 -Recommended, 2 - Required in some public spaces, 3 - Required in all public spaces, 4 -Required outside-the-home at all times 
- MeanFacialCoverings - This is the avereage facial coverings restriction level for each country.
- MaxStayHome - This is the maximal stay at home restriction level for each country which ranges from 0 - 3 (strictest) . NA - No data, 0 - No measures, 1 - Recommended, 2 - Required (except essentials) , 3 - Required (few exceptions).
- MeanStayHome - This is the average stay at home restriction level for each country.


***Programmatic Approach:***
Our dataset was loaded, cleaned and analysed using R Studio.

These steps were undertaken: 
1. Downloading the csv datasets from GitHub.
2. Reading the csv datasets in R Studio using read.csv() function and UTF-8-BOM file encoding.
3. Joining the datasets into 1 using join() functions.
4. Transforming the dataset into Json Format (WILL BE DONE)
5. Importing RAW dataset to MongoDB (WILL BE DONE)
6. Extracting the dataset from MongoDB as a csv file
7. Reading the csv file in R Studio again.
8. Analysing and visualising the data.
9. Writing the final dataset into a csv file which will be later used in the multiple linear regression.


### Slovakia Testing Dataset - Maria Migrova ###
This dataset consists of a data about number of tests performed in Slovakia by different gender and age group.

This dataset consists of: 
- Date
- Region 
- District
- District Code
- Gender
- Age Group ( 1 = 00 -19, 2 = 20 -34, 3 = 35 - 54, 4 = 55 - ...)
- PCR Pos - number of positive tests
- PCR Neg - number of negative tests
- PCR Total - total number of tests performed

***Programmatic Approach:***
Our dataset was loaded, cleaned and analysed using R Studio.

These steps were undertaken: 
1. Downloading the csv dataset from GitHub.
2. Reading the csv dataset in R Studio using read.csv() function and UTF-8-BOM file encoding.
3. Transforming the dataset into Json Format (WILL BE DONE)
4. Importing RAW dataset to MongoDB (WILL BE DONE)
5. Extracting the dataset from MongoDB as a csv file
6. Reading the csv file in R Studio again.
7. Analysing and visualising the data. Creating a Random Forest Model, which shows how different age group and gender influance the number of positive tests.
9. Writing the final dataset into a csv file. This file won't be used for the final linear regression.

## *Authors:* ##
- Alun Price
- Maria Migrova
- Polina Prinii


