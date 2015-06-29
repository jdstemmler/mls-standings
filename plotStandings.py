from __future__ import division

import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import seaborn as sns


panel = os.path.join('./data/mlsStandings.data')
P = pd.read_hdf(panel, 'shield')

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

standings = P[:,:,'PTS']
dates = standings.columns.to_pydatetime()
standings = standings.sort(dates[-1], ascending=False)
clubs = standings.index.tolist()

colordict = read_colors(colors)
confdict = read_conference(conferences)

for club in clubs:
    ax.plot_date(dates, standings.ix[club].values, '-',
                 label=club, color=colordict[club])
    #standings.ix[club].plot('.-', ax=ax, label=club)

ax.legend(bbox_to_anchor=(1, .5), loc='center left',
          borderaxespad=0., fontsize=8)
ax.set_ylim(top = ax.get_ylim()[-1]+5)
ax.set_ylabel('Points')

fig.suptitle("Current MLS Supporter's Shield Standings\nAs of {} Eastern"
             .format(dates[-1]))
fig.autofmt_xdate()
fig.savefig('./plots/standings_history.png', dpi=300)


fig = plt.figure()
ax = fig.add_subplot(111)

for i, club in enumerate(clubs):
    if confdict[club] == "Western":
        scale = -1
        ha = 'right'
    elif confdict[club] == "Eastern":
        scale = 1
        ha = 'left'

    points = standings[dates[-1]].ix[club]

    ax.barh(-1*i, scale*points, align='center',
            color=confcolors[confdict[club]])
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
ax.set_title('MLS Standings by Conference\nAs of {} Eastern'.format(dates[-1]))

fig.savefig('./plots/standings_current.png')

plt.close('all')
