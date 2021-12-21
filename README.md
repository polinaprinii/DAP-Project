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

### Testing Dataset, Restrictions Dataset, Slovakia Testing Dataset - Maria Migrova ###
The goal of this datasets is to summarise the number of tested people by each country and different restriction levels.

This datasets consists of: <br/>
TESTING DATASET:
- isocode of each country
- country name
- tests = the total number of tests performed by each country in total from 01/01/2021 - 24/11/2021 <br/>
RESTRICTIONS DATASET:
- isocode of each country
- country name
- MaxStringencyIndex - This is the maximal stringency index for each country which ranges from 0 - 100 (strictest). It is based on nine response indicators including school closures, workplace closures and travel bans.
- MeanStringencyIndex - This is the average stringency index for each country from 01/01/2021 - 24/11/2021
- MaxFacialCoverings - This is the maximal facial coverings restriction level for each country. It ranges from 0 - 4 (strictest). NA - No data, 0- No policy, 1 -Recommended, 2 - Required in some public spaces, 3 - Required in all public spaces, 4 -Required outside-the-home at all times 
- MeanFacialCoverings - This is the avereage facial coverings restriction level for each country.
- MaxStayHome - This is the maximal stay at home restriction level for each country which ranges from 0 - 3 (strictest) . NA - No data, 0 - No measures, 1 - Recommended, 2 - Required (except essentials) , 3 - Required (few exceptions).
- MeanStayHome - This is the average stay at home restriction level for each country.<br/>
SLOVAKIA TESTING DATASET:
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
Our datasets were loaded, cleaned and analysed using R Studio. 

These steps were undertaken:
1. Downloading the csv dataset from GitHub.
2. Reading the csv dataset in R Studio using read.csv() function and UTF-8-BOM file.
3. Analysing and visualising the data.
4. Writing the final dataset into a csv file which will be later used for the multiple linear regression.
5. Uploading the final dataset into MongoDB using mongo() function.


### Global Confirmed Cases and Death Rates - Alun Price ###
This section of the project aims to utilise a data pipeline to extract, transform and load the cumulative data available from COVID-19 Data Repository by the Center for Systems Science and Engineering (CSSE) at Johns Hopkins University.
This data begins on the 22nd of January 2020 and continues  to the current date.

Once the data has been scraped from the GitHub repository it is stored within mongoDB, then transformed and an explorotory data analysis is performed before finally visualizations are created to explore the countries with the highest deaths and also the highest number of confirmed cases to date.

this section was completed using:
- python programming language written within PyCharm
- MongoDB running a Debian instance within a Virtual Machine on Virtual Box
- Postgrsql running also on a Debian instance on a virtual machine on Virtual Box

The Data Pipeline is as follows:

**Step One:** The RAW data files are scraped using pandas and then stored locally <br />
**Step Two:** The RAW files are then converted to dictionaries and programmatically stored within MongoDB <br />
**Step Three:** The Data is retrieved from MongoDB and transformed, creating two global files of Confirmed cases and deaths globally. <br />
**Step Four:** The Transformed data is then stored again in MongoDB <br />
**Step Five:** The transformed data is retrieved from MongoDB and an exploratory data analysis is performed to determine the countries with the highest Death rates and also the highest case rates. <br />
**Step Six:** A Number of Visualizations are generated of the highest scoring countries. An interactive map of the world is also generated showing the total values of both cases and deaths worldwide as of today's date. <br />
**Step Seven:** A file representing a snapshot of cases and deaths worldwide to date is also scraped programmatically from the same source and is transformed  <br />
**Step Eight:** this transformed file is then stored in a postgreSQL database also running on a Debain instance on Virtual Box <br />

All Files and Visualizations can be seen within the "Data" and "Visualizations" Folders and are updated whenever the "Master.py" File is executed.

## *Authors:* ##
- Alun Price
- Maria Migrova
- Polina Prinii


