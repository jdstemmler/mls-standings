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
ax.set_xlabel("Points")
fig.savefig('./plots/current_points_standings.png', dpi=300)

# make the bar chart with points at the current game and total points
level_game_points = T.dropna(how='any', axis=0)
level_games = level_game_points.index[-1]
level_game_points = level_game_points.sum()
level_game_points.sort(ascending=False)

fig, ax = mlsPlots.plot_split_standings(level_game_points, conferences,
                                        secondary=points)
ax.set_title("MLS Club Standings by Conference\nGame {:2.0f}"
             .format(level_games))
ax.set_xlabel('Points')
fig.savefig('./plots/level_game_points_standings.png', dpi=300)

ppg = T.sum() / T.count()
ppg.sort(ascending=False)

fig, ax = mlsPlots.plot_split_standings(ppg, conferences, xtickfmt='{:2.1f}')
ax.set_title('MLS Club Standings by Conference\nPoints per Game')
ax.set_xlabel('Points per Game')
fig.savefig('./plots/ppg_standings.png', dpi=300)
