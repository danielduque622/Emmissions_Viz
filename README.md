# Countries' Emissions and their Impact on Temperataure

The following is an application that allows you to analyze the output of countries' emissions through the last century and its impact on temperature:

[World Emissions Visualized](https://emmissionsviz-ekrmossc8qybkmrpccragb.streamlit.app/)

## Introduction  

In the last half a decade the topic of climate change has been predominant among the political and scientiic communities. My aim with this application was not to assert any views but rather to allow the user to explore and compare how different countries have impacted the output of different types of emissions. The user can also see the impact that these emissions have on temperature and they can analyze any potential correlations (which are not necessarily causal) between emissions, poulation, GDP, etc. 

## Data Operation/Abstraction Design

Data was optained from our world in data:

[World Emissions Data](https://ourworldindata.org/co2-and-greenhouse-gas-emissions#explore-data-on-co2-and-greenhouse-gas-emissions)

The dataset was very comprehensive and clean since it has already been prepped for analysis, so my focus was mainly on the visualizations. I created four different "pages" on the website. The first two pages are for emission and temperature analysis - they display a series of visualizations for each topic accordingly and they can be filtered by country, year and emission type. The third page is a correlation analysis which can be filtered by country, range, and any dataset column. Lastly there is a data dictionary which describes all of the 'columns' as there is some domain lingo used in this dataset. Each column here also provides a specifc source for where the records were obtained. 

## Future Work 

In future work it would be intereing to analyze which countries have chosen to implement climate related policies and what impacts that may have had on their emission outputs as well the economic impact on GDP. 
