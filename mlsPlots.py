from __future__ import division

import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import seaborn as sns

# read in the color table
def read_colors(colors):
    colortable = pd.read_csv(colors, header=0, index_col="Club")
    colordict = {}
    for club, r, g, b in colortable.itertuples():
        colordict[club] = (r/255., g/255., b/255.)
    return colordict

# read in the conference table
def read_conference(conferences):
    conftable = pd.read_csv(conferences, header=0, index_col="Club")
    confdict = {}
    for club, conference in conftable.itertuples():
        confdict[club] = conference.strip()
    return confdict

# make a timeseries like plot of points against games played
def plot_points_by_game(table, colors):

    # make the figure and axes
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_axes([.1, .1, .7, .8])

    # get the current point stanings for the ordered list of clubs
    current_points = table.sum().copy()
    current_points.sort(ascending=False)
    clubs = current_points.index.tolist()

    # get the colors for each club
    color_dict = read_colors(colors)

    # iterate through each club and plot
    for club in clubs:
        club_points = table[club].cumsum()
        ax.plot(club_points.index, club_points.values, '.-',
                label=club, color=color_dict[club])

    # make the legend
    ax.legend(bbox_to_anchor=(1, .5), loc='center left',
              borderaxespad=0., fontsize=8)

    ax.set_ylim(top = ax.get_ylim()[-1]+5)
    ax.set_xlabel('Games Played')
    ax.set_ylabel('Points')

    ax.set_title("Current MLS Supporter's Shield Standings")

    # return the figure and axes handles for doing extra things
    return fig, ax

# make the bar chart
def plot_split_standings(primary, conferences, secondary=None, **kwargs):

    # create the figure and axis handles
    fig, ax = plt.subplots()

    # generate the list of clubs based on the primary Series
    clubs = primary.index.tolist()

    # get the conference mapping
    conference_dict = read_conference(conferences)
    conference_colors = {'Western': '#FA5858',
                         'Eastern': '#81BEF7'}

    # set up counters for playoff designation
    west_playoff, east_playoff = (0, 0)

    # loop through each of the clubs
    for i, club in enumerate(clubs):
        # get the conference each club belongs to and set some variables
        conference = conference_dict[club]
        if conference == "Western":
            flip = -1
            ha = 'right'
            if west_playoff is not None: west_playoff += 1
        elif conference == "Eastern":
            flip = 1
            ha = 'left'
            if east_playoff is not None: east_playoff += 1

        # the the primary values for the specific club
        primary_value = primary[club]

        # if there's a secondary parameter, plot that first
        if secondary is not None:
            secondary_value = secondary[club]
            ax.barh(-1*i, flip*secondary_value, align='center',
                    color=conference_colors[conference],
                    edgecolor=conference_colors[conference],
                    alpha=.3)

        # plot the primary parameters
        ax.barh(-1*i, flip*primary_value, align='center',
                color=conference_colors[conference],
                edgecolor=conference_colors[conference],
                alpha=1)

        # draw the playoff cutoff lines
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

        # write the team names to the bars
        offset = flip * (ax.get_xlim()[1] / 40)
        ax.text(0, -1*i, club, ha=ha, va='center', fontsize=8)

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
