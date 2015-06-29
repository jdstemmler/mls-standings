from __future__ import division

import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import seaborn as sns


panel = os.path.join('./data/mlsStandings.data')
table = os.path.join('./data/resultsTable.csv')

P = pd.read_hdf(panel, 'shield')
T = pd.read_csv(table, index_col="Game")

colors = os.path.join('./assets/teamColors.csv')
conferences = os.path.join('./assets/conferences.csv')

confcolors = {'Western': '#FA5858',
              'Eastern': '#81BEF7'}

def read_colors(colors):
    colortable = pd.read_csv(colors, header=0, index_col="Club")
    colordict = {}
    for club, r, g, b in colortable.itertuples():
        colordict[club] = (r/255., g/255., b/255.)
    return colordict

def read_conference(conferences):
    conftable = pd.read_csv(conferences, header=0, index_col="Club")
    confdict = {}
    for club, conference in conftable.itertuples():
        confdict[club] = conference.strip()
    return confdict

fig = plt.figure()
ax = fig.add_axes([.1, .1, .6, .8])

current_points = T.sum().copy()
current_points.sort(ascending=False)
clubs = current_points.index.tolist()

colordict = read_colors(colors)
confdict = read_conference(conferences)

for club in clubs:
    club_standing = T[club].cumsum()
    ax.plot(club_standing.index, club_standing.values, '.-',
                 label=club, color=colordict[club])
    #standings.ix[club].plot('.-', ax=ax, label=club)

ax.legend(bbox_to_anchor=(1, .5), loc='center left',
          borderaxespad=0., fontsize=8)
ax.set_ylim(top = ax.get_ylim()[-1]+5)
ax.set_xlabel('Games Played')
ax.set_ylabel('Points')

ax.set_title("Current MLS Supporter's Shield Standings\nAs of {} Eastern"
             .format(P.items[-1]))
#fig.autofmt_xdate()
fig.savefig('./plots/standings_history.png', dpi=300)


fig = plt.figure()
ax = fig.add_subplot(111)
wp, ep = (0, 0)

for i, club in enumerate(clubs):
    if confdict[club] == "Western":
        scale = -1
        ha = 'right'
        if wp is not None: wp += 1
    elif confdict[club] == "Eastern":
        scale = 1
        ha = 'left'
        if ep is not None: ep += 1

    points = current_points.ix[club]

    ax.barh(-1*i, scale*points, align='center',
            color=confcolors[confdict[club]],
            edgecolor='none')

    if wp == 6:
        ax.plot([0, ax.get_xlim()[0]], [-1*i-.5, -1*i-.5], 'k--', linewidth=.5)
        wp = None
    if ep == 6:
        ax.plot([0, ax.get_xlim()[1]], [-1*i-.5, -1*i-.5], 'k--', linewidth=.5)
        ep = None

    ax.text(scale*2, -1*i, club, ha=ha, va='center', fontsize=8)
    ax.text(scale*(points+1), -1*i, '{:2.0f}'.format(points),
            ha=ha, va='center', fontsize=9)

ax.set_ylim(top=1)
ax.set_xticklabels(['{:2.0f}'.format(xt) for xt in abs(ax.get_xticks())])
ax.set_yticklabels([])
ax.set_xlabel('Points')
ax.grid('off', axis='y')
ax.set_ylabel('Western Conference')
ax2 = ax.twinx()
ax2.set_ylabel('Eastern Conference')
ax2.grid('off')
ax2.set_yticks([])
ax.set_title('MLS Standings by Conference\nAs of {} Eastern'.format(P.items[-1]))

fig.savefig('./plots/standings_current.png', dpi=300)

plt.close('all')
