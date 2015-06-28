from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import pandas as pd
import datetime
import os

panel = os.path.join('./mlsStandings.data')
has_panel = os.path.isfile(panel)

url = "http://www.mlssoccer.com/standings/supporters-shield"
html = urlopen(url)
listingObj = BeautifulSoup(html.read())
update = listingObj.findAll("div", {"class": "standings-last-update"})[0].contents[0].strip().split('Updated:')[-1].strip()
last_update = datetime.datetime.strptime(update, '%m/%d/%y at %I:%M %p')

table = listingObj.findAll("table", {"class": "standings-table"})[0]
rows = table.findAll("tr")

headers = [r.contents[0].strip() for r in rows[0].findChildren("th")]
data = None
ranks = []

for row in rows[1:]:
	if data is None:
		data = {}
	
	ranks.append(int(row.findChild("td", {"class": "first"}).contents[0].strip()))
	club = row.findChild("a").contents[0].strip()
	values = [float(r.contents[0].strip()) for r in row.findChildren("td")[2:]]
	
	for k, v in zip(headers[1:], [club]+values):
		if k not in data.keys():
			data[k] = []
		
		data[k].append(v)

D = pd.DataFrame(data, index=ranks)

if not has_panel:
	P = pd.Panel({last_update: D})
elif has_panel:
	P = pd.read_hdf(panel, 'data')
	P[last_update] = D

P.to_hdf(panel, 'data')