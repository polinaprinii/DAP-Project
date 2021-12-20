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