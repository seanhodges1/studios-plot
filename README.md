# River water level plot widget

## Problem statement

Agencies monitoring river levels, and providing information to the public, use a methods to present this data. Typically, graphs a generated showing a 7 day time frame of river water level changes. These graphs are either static and generated on fly, or interactive and taking data directly from some authoritative source.

ESRI's ArcGIS Online platform contains a convenient framework for the creation of dashbaoards. The dashboarding framework allows for a combination of maps, tables, charts, lists, cards, externally embedded content, etc, that can be interacted with by a user. The expectation is that all data is resident, or available to, the ArcGIS platform. For data that exists on other platforms (such as time series), hosting this in the ArcGIS space is not practical.

Making a river water level plot, from data in a time series system, that can be interacted with as any other native ESRI widget is not trivial exercise using the ArcGIS platform alone. A method to resolve this is to use the externally embedded content option. 

The challenge that this code is trying to resolve is that of:
* making a given time series data plot available as embedded content
* having the embedded content linked to other selections on the dashboard
* having it appear as native content that can then be interacted with by the user

## Method

The Dash framework by Plotly (https://dash.plotly.com/introduction) has been selected as a method to resolve this probem.
