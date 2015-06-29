from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import os

# set the location of the data file
panel = os.path.join('./data/mlsStandings.data')
has_panel = os.path.isfile(panel)

def wld2pts(wld):
	if wld == 'W':
		pts = 3
	elif wld == 'L':
		pts = 0
	elif wld == 'D':
		pts = 1
	elif wld == '':
		pts = None

	return pts

def results_table():
	url = "http://www.mlssoccer.com/results"
	html = urlopen(url)
	listingObj = BeautifulSoup(html.read())

	table = listingObj.findAll("table", {"class": "game-record"})[0]
	rows = table.findAll("tr")
	games = [r.contents[0].strip() for r in rows[0].findAll("td")]
	record = {}
	for row in rows[1:]:
		cols = row.findAll("td")
		club = cols[0].findChild("div").contents[0].strip()
		club_record = []
		for col in cols[1:]:
			wld = col.findChild("a").contents[0].strip()
			club_record.append(wld2pts(wld))
		record[club] = club_record

	D = pd.DataFrame(record, index=games[1:])
	D.to_csv('./data/resultsTable.csv', index_label="Game")
	return D

def supporters_shield(panel, has_panel):
	# defile the url for the supporters shield standings
	url = "http://www.mlssoccer.com/standings/supporters-shield"
	html = urlopen(url)
	listingObj = BeautifulSoup(html.read())

	# get the last updated time and convert to python datetime
	update = (listingObj.findAll("div", {"class": "standings-last-update"})[0]
				.contents[0]
				.strip()
				.split('Updated:')[-1]
				.strip())
	last_update = datetime.datetime.strptime(update, '%m/%d/%y at %I:%M %p')

	# get the standings table and find all rows
	table = listingObj.findAll("table", {"class": "standings-table"})[0]
	rows = table.findAll("tr")

	# pull out the headers
	headers = [r.contents[0].strip() for r in rows[0].findChildren("th")]

	# initialize data structures
	data = None
	clubs = []

	# iterate through each row, add to data dictionary
	for row in rows[1:]:
		if data is None:
			data = {}

		rank = (int(row.findChild("td", {"class": "first"})
							.contents[0]
							.strip()))

		clubs.append(row.findChild("a").contents[0].strip())
		values = [float(r.contents[0].strip()) for r in row.findChildren("td")[2:]]

		for k, v in zip(['rank']+headers[2:], [rank]+values):
			if k not in data.keys():
				data[k] = []

			data[k].append(v)

	# save the data to a DataFrame
	D = pd.DataFrame(data, index=clubs).sort()

	# check for the Panel. Create if it doesn't exist.
	if not has_panel:
		P = pd.Panel({last_update: D})
	elif has_panel:
		P = pd.read_hdf(panel, 'shield')
		P[last_update] = D

	# write the panel out to file.
	P.to_hdf(panel, 'shield')

	return P

P = supporters_shield(panel, has_panel)
D = results_table()
