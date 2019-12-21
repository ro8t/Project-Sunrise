# Dependencies
import pandas as pd
from fredapi import Fred

# API Keys
from config import fred

# Creating FRED API connection
derf = Fred(api_key=fred)

# Creating df of gdp per capita's
# Millions of Dollars, Annual, Not Seasonally Adjusted 2001-2017

gdp_observations = derf.get_series('NGMP41860', 
									observation_start='2001-01-01', 
                             		observation_end='2017-01-01').index

# GDP per capita for cities in the US
cities_gdp = pd.DataFrame(
{
    "Observation": [o for o in gdp_observations],
    "Bay Area": [bay for bay in derf.get_series('NGMP41860', 
    											observation_start='2001-01-01', 
                                            	observation_end='2017-01-01')],
    "San Jose": [sj for sj in derf.get_series('NGMP41940', 
    										   observation_start='2001-01-01', 
                                               observation_end='2017-01-01')],
    "Austin": [aus for aus in derf.get_series('NGMP12420',
    										   observation_start='2001-01-01', 
                                               observation_end='2017-01-01')],
    "New York": [ny for ny in derf.get_series('NYNGSP', 
    										   observation_start='2001-01-01', 
                                               observation_end='2017-01-01')],
    "Boston": [bos for bos in derf.get_series('NGMP14460', 
    										   observation_start='2001-01-01', 
                                               observation_end='2017-01-01')],
    "Chicago": [chi for chi in derf.get_series('NGMP16980', 
    											observation_start='2001-01-01', 
                                            	observation_end='2017-01-01')],
    "Denver": [den for den in derf.get_series('NGMP19740', 
    										   observation_start='2001-01-01', 
                                               observation_end='2017-01-01')],
    "Los Angeles": [la for la in derf.get_series('NGMP31080', 
    											  observation_start='2001-01-01', 
                                            	  observation_end='2017-01-01')],
    "Seattle": [sea for sea in derf.get_series('NGMP42660', 
    											observation_start='2001-01-01', 
                                            	observation_end='2017-01-01')],
})

# CPI df - monthly, seasonally adjusted 1970 - 2018
cpi_observations = derf.get_series('CPIAUCSL', 
									observation_start='1985-01-01', 
                                    observation_end='2018-01-01').index
# CPI's for various US markets
cpi_df = pd.DataFrame(
{
    "Observation": [o for o in cpi_observations],
    "All Items": [a for a in derf.get_series('CPIAUCSL', 
    										  observation_start='1985-01-01', 
                                              observation_end='2018-01-01')],
    "All Items Less Food and Energy": [fe for fe in derf.get_series('CPILFESL', 
                                                                     observation_start='1985-01-01', 
                                                                     observation_end='2018-01-01')],
    "Medical Care": [mc for mc in derf.get_series('CPIMEDSL', 
    											   observation_start='1985-01-01', 
                                                   observation_end='2018-01-01')],
    "Rent of Primary Residence": [rent for rent in derf.get_series('CUSR0000SEHA', 
                                                                    observation_start='1985-01-01', 
                                                                    observation_end='2018-01-01')],
    "Food and Beverages": [fb for fb in derf.get_series('CPIFABSL', 
    													 observation_start='1985-01-01', 
                                                         observation_end='2018-01-01')],
    "New Vehicles": [nv for nv in derf.get_series('CUSR0000SETA01', 
    											   observation_start='1985-01-01', 
                                                   observation_end='2018-01-01')],
    "Housing": [house for house in derf.get_series('CPIHOSSL', 
    												observation_start='1985-01-01', 
                                                 	observation_end='2018-01-01')]

})

