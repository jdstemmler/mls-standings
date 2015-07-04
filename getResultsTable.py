from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import os

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

def results_table(outfile):
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
	D.to_csv(outfile, index_label="Game")
	return D

#print(__name__)
if __name__ == "__main__":
	outfile = os.path.join('./data/resultsTable.csv')
	# print('saving {}'.format(outfile))
	D = results_table(outfile)
