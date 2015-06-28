import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

panel = os.path.join('./data/mlsStandings.data')
P = pd.read_hdf(panel, 'data')

fig = plt.figure()
ax = fig.add_axes([.1, .1, .6, .8])

clubs = P.major_axis.tolist()
standings = P[:,:,'PTS']
dates = standings.columns.to_pydatetime()

for club in clubs:
    ax.plot_date(dates, standings.ix[club].values, '.-', label=club)
    #standings.ix[club].plot('.-', ax=ax, label=club)

ax.legend(bbox_to_anchor=(1, 1), loc=2, borderaxespad=0., fontsize=9)
ax.set_ylim(top = ax.get_ylim()[-1]+5)
ax.set_ylabel('Points')

fig.suptitle('Current MLS Standings\nAs of {}'.format(dates[-1].date()))
fig.autofmt_xdate()
fig.savefig('./plots/standings.png', dpi=300)
