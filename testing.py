#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 28 19:38:59 2021

@author: shodges
"""

import requests
import sys
import pandas as pd
import xmltodict

sys.path.append("/Users/shodges/Documents/GitHub/hilltop-py/hilltoppy/")
import web_service as ws

### Parameters
base_url = 'http://tsdata.horizons.govt.nz/'
hts = 'boo.hts'
request = 'DataTable'
collection = 'River Level'
site = 'Manawatu at Teachers College'
measurement = 'Stage [Water Level]'
from_date = '2021-06-28 00:00'
to_date = '2021-06-29 00:00'
#dtl_method = 'trend'

url = ws.build_url(base_url=base_url, hts=hts, request=request, collection=collection, from_date=from_date, to_date=to_date)
url = url + "&from=" + from_date + "&to=" + to_date
print(url)


resp = requests.get(url, timeout=300)
data = xmltodict.parse(resp.text)['HilltopServer']['Results']
df = pd.DataFrame(data)

