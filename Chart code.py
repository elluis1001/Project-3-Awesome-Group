import json
from pathlib import Path
from typing import Union
from collections import defaultdict

import pandas as pd
import requests
import os

from bokeh.models.tools import HoverTool
from bokeh.plotting import figure, output_file, show, save, ColumnDataSource
from bokeh.transform import factor_cmap
from bokeh.palettes import Blues8




filepath = Path("data_query\electric_stations_by_state.json")
with open(filepath, encoding="utf-8") as jsonfile:
    electric_stations_by_state_json = json.load(jsonfile)


stations_by_state_df = pd.DataFrame(electric_stations_by_state_json, index=[0])
stations_by_state_df.head()

List = list(electric_stations_by_state_json.items())

stations_by_state_df2 = pd.DataFrame(List, columns=["State", "EV Stations"])

stations_by_state_df2

# State = stations_by_state_df2['State']
# EV_Stations = stations_by_state_df2['EV Stations']

# Create ColumnDataSource from data frame
source = ColumnDataSource(stations_by_state_df2)

output_file('index.html')

# State list
state_list = source.data['State'].tolist()

#  add plot
chart = figure(
        y_range=state_list,
        width=800,
        height=600,
        title='EV Stations by State',
        x_axis_label='EV Stations',
        tools="pan,box_select,zoom_in,zoom_out,save,reset"
) 

# Render glyph
chart.hbar(y='State',
           right='EV Stations',
           left=0,
           height=0.7, 
           fill_color=factor_cmap('State',
                                  palette=Blues8,
                                  factors=state_list
           ),
           fill_alpha=0.9,
           source=source
)

# Add Tooltips
hover = HoverTool()
hover.tooltips ="""
    <div>
        <h3>@State</h3>
        <div><strong>EV Stations: </strong>@EV Stations</div>
`   </div>
"""
chart.add_tools(hover)

              
# show results
# show(chart)

# Save file
save(chart)
