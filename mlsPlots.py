from __future__ import division

import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import seaborn as sns

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

def plot_points_by_game(table, colors):
    fig = plt.figure()
    ax = fig.add_axes([.1, .1, .6, .8])

    current_points = table.sum().copy()
    current_points.sort(ascending=False)

    clubs = current_points.index.tolist()

    color_dict = read_colors(colors)

    for club in clubs:
        club_points = table[club].cumsum()
        ax.plot(club_points.index, club_points.values, '.-',
                label=club, color=color_dict[club])

    ax.legend(bbox_to_anchor=(1, .5), loc='center left',
              borderaxespad=0., fontsize=8)

    ax.set_ylim(top = ax.get_ylim()[-1]+5)
    ax.set_xlabel('Games Played')
    ax.set_ylabel('Points')

    ax.set_title("Current MLS Supporter's Shield Standings")

    return fig, ax

def plot_split_standings(primary, conferences, secondary=None, **kwargs):

    fig, ax = plt.subplots()

    clubs = primary.index.tolist()

    conference_dict = read_conference(conferences)
    conference_colors = {'Western': '#FA5858',
                         'Eastern': '#81BEF7'}

    west_playoff, east_playoff = (0, 0)

    for i, club in enumerate(clubs):
        conference = conference_dict[club]
        if conference == "Western":
            flip = -1
            ha = 'right'
            if west_playoff is not None: west_playoff += 1
        elif conference == "Eastern":
            flip = 1
            ha = 'left'
            if east_playoff is not None: east_playoff += 1

        primary_value = primary[club]
        if secondary is not None:
            secondary_value = secondary[club]
            ax.barh(-1*i, flip*secondary_value, align='center',
                    color=conference_colors[conference],
                    edgecolor='none',
                    alpha=.3)

        ax.barh(-1*i, flip*primary_value, align='center',
                color=conference_colors[conference],
                edgecolor='none',
                alpha=1)

        if west_playoff == 6:
            ax.plot([0, ax.get_xlim()[0]],
                    [-1*i-.5, -1*i-.5],
                    'k--', linewidth=.6)
            west_playoff = None
        elif east_playoff == 6:
            ax.plot([0, ax.get_xlim()[1]],
                    [-1*i-.5, -1*i-.5],
                    'k--', linewidth=.6)
            east_playoff = None

        ax.text(0, -1*i, ' '+club+' ', ha=ha, va='center', fontsize=8)

    ax.set_ylim(top=1)
    xtickfmt = kwargs.pop('xtickfmt', '{:2.0f}')
    ax.set_xticklabels([xtickfmt.format(xt) for xt in abs(ax.get_xticks())])
    ax.set_yticklabels([])
    ax.grid('off', axis='y')

    ax.set_ylabel('Western Conference')
    ax2 = ax.twinx()
    ax2.set_ylabel('Eastern Conference')
    ax2.grid('off')
    ax2.set_yticks([])

    ax.set_title('MLS Standings by Conference')

    return fig, ax
