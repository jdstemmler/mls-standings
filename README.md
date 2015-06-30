# MLS Standings
###Major League Soccer - Race to the Supporter's Shield

This is a simple little web scraping and plotting exercise. It goes out to the MLS Soccer website and gets the most recent standings table. It then makes some (hopefully) interesting plots.

Please know that this is rather rough around the edges. There is no documentation other than some inline comments. This README will serve as the official documentation for the time being.

## Useage

### Getting the Data
The data is collected by running the `getResultsTable.py` script. This scrip goes out to the [MLS Results Map](http://www.mlssoccer.com/results) page and pulls down the table. It then converts the W/L/D information into points - this is how I can get cumulative points for each game. After getting the table, it then writes out to data/resultsTable.csv so that plotting can happen without scraping the MLS website over and over. So, if you're just wanting to play with the data, there's no need to run the getResultsTable.py script.

### Plotting the Data
Plotting the data happens in the `makePlots.py` script. This script uses some plots defined in `mlsPlots.py`. If you're wanting to take a look at how the plots are constructed, you could poke around in the mlsPlots file. makePlots is slightly less interesting, but demonstrates how to get the data out of the csv file and into the plotting routines. It also demonstrates how to save the plots locally.

## Notes
### Required Packages
* Python3
* Pandas
* Matplotlib
* Seaborn
* BeautifulSoup4

### Disclaimer
I make no guarantees that this will work. Please don't run the web scraping script over and over on MLS's website - that's a great way to irritate them and is not very nice.

## Plots
For more plots, go poke around the plots directory!
#### Current Standings
![CurrentStandings](./plots/current_points_standings.png =500x)

#### Standings by Game
![StandingsByGame](./plots/standings_by_game.png =500x)