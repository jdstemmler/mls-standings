import mlsPlots
import os
import pandas as pd

table = os.path.join('./data/resultsTable.csv')
T = pd.read_csv(table, index_col="Game")

colors = os.path.join('./assets/teamColors.csv')
conferences = os.path.join('./assets/conferences.csv')

# Make the line plot with all the teams and points for each game
fig, ax = mlsPlots.plot_points_by_game(T, colors)
fig.savefig('./plots/standings_by_game.png', dpi=300)

# make the bar chart of total current points
points = T.sum().copy()
points.sort(ascending=False)

fig, ax = mlsPlots.plot_split_standings(points, conferences)
ax.set_title("MLS Club Standings by Conference\nTotal Current Points")
fig.savefig('./plots/current_points_standings.png', dpi=300)

level_game_points = T.dropna(how='any', axis=0)
level_games = level_game_points.index[-1]
level_game_points = level_game_points.sum()
level_game_points.sort(ascending=False)

fig, ax = mlsPlots.plot_split_standings(level_game_points, conferences,
                                        secondary=points)
ax.set_title("MLS Club Standings by Conference\nGame {:2.0f}"
             .format(level_games))
fig.savefig('./plots/level_game_points_standings.png', dpi=300)
