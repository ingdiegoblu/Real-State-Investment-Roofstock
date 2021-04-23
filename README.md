# Real-State-Investment-Roofstock

Project Overview
•	Scraped data over a quantity of properties in the market from roofstock website using python and selenium.
•	Developed a method of evaluation that consider the best option to invest in.

Code and Resources Used
Python Version: 3.7
Packages: pandas, numpy, sklearn, matplotlib, seaborn, selenium, folium, geopy, geocoder

Web Scraping
I coded a script using selenium library to scrape roofstock.com website. From each property I got the following variables which were separated in 2 different csv file:
•	Street
•	City 
•	State
•	Zip
•	Rooms (number of bedrooms and bathrooms)
•	sqft area
•	Built in (year)
•	Price
•	Current Rents
•	Cap Rate
•	Cash flow (First year net cash estimated in dollar after payment for property taxes, property management, loan payments, etc.)
•	Rating
•	Links
Highlights of each of property(status or condition):
•	Roof
•	Attic
•	Bathrooms
•	Basement
•	HVAC
•	Bedrooms
•	Electrical
•	Exterior       
•	Garage         
•	Plumbing       
•	Landscaping    
•	Structural     
•	Kitchen        

Data Cleaning
The cleaning process is important before creating any model. I divided it into 2 parts: the first one for a clustering approximation using DBSCAN and the second one for predictions using a regression model. Key factors that I considered:
I Part
•	Split ‘Room column’ to separate the number of bedrooms individually from the number of bathrooms.
•	Extraction of impractical symbols(i.e  $ %) from dataframe and conversion of object type into int(number) type.
•	Links column is just only a reference of the Property URL, in this case, is not important for analysis so we can drop it.
•	Obtention of longitude and latitude data through Geopy library
II Part
•	Factorize States by converting them into representative numerical values.
•	Load the highlights data of the houses and map their values( ‘—’ : 1, ‘Functional’:2,’Needs repair’:1)
•	Concatenation of all the parameters

Model Building
The model building was divided also into 2 parts:
I Part - DBSCAN Clustering model: segmentation of states based on Cap rate.
II Part - Predictive Model based on Cap Rate.
