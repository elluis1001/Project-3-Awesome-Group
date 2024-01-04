import json
from pathlib import Path
from typing import Union
from collections import defaultdict
import hvplot.pandas
import pandas as pd
import requests
import os
from scipy.stats import linregress
from bokeh.models import HoverTool
from bokeh.plotting import figure, output_file, show
from citipy import citipy

api_key = 'AWMepE53xJxr8Qu8yP3w6J6PLAf3ye6sO7Fsdvlc'
base_url = 'https://developer.nrel.gov/api/alt-fuel-stations/v1.json'

# List of all US state codes
state_codes = [
    'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA',
    'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK',
    'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'
]

# List of attributes to retrieve, including the new ones
attributes_to_retrieve = [
    'id', 'station_name', 'street_address', 'city', 'state', 'zip',
    'latitude', 'longitude', 'owner_type_code', 'ev_connector_types', 'ev_pricing',
    'geocode_status', 'access_code', 'ev_level1_evse_num', 'ev_level2_evse_num', 'ev_dc_fast_num', 'ev_other_evse'
]

# List to store detailed information for stations meeting the criteria
filtered_stations = []

for state_code in state_codes:
    query_params = {
        'fuel_type_code': 'ELEC',
        'state': state_code,
        'country': 'US',
        'restricted_access': 'false',  # Add restricted_access parameter
        'api_key': api_key
    }

    # Make the API request
    response = requests.get(base_url, params=query_params)

    # Parse the JSON response
    data = response.json()

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Add detailed information for each station meeting the criteria
        filtered_stations.extend([
            {attr: station[attr] for attr in attributes_to_retrieve}
            for station in data.get('fuel_stations', [])
        ])

    else:
        # Print an error message if the request was not successful
        print(f'Error: {response.status_code} - {response.text}')

# # Print the total count of electric vehicle stations in the US after filtering
# total_us_stations = sum(len(data.get('fuel_stations', [])) for state_code in state_codes)
# print(f'Total electric vehicle stations in the US after filtering: {total_us_stations}')


california_df = pd.DataFrame(filtered_stations)

california_df = california_df[california_df['state'] == 'CA']

california_df

