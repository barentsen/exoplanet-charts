"""Creates beautiful visualizations of the publication database."""
import datetime
import sqlite3 as sql

import numpy as np
from astropy import log

from matplotlib import pyplot as plt
import matplotlib.patheffects as path_effects
import matplotlib as mpl
from matplotlib import style
import seaborn as sns

from kpub import PublicationDB

MISSIONS = ['k2']
SCIENCES = ['exoplanets', 'astrophysics']

output_fn = 'publications-per-year-k2.png'
db = PublicationDB()
first_year = 2014
barwidth = 0.75
extrapolate = True
current_year = datetime.datetime.now().year


palette = sns.color_palette(['#f1c40f', '#2980b9'])
style.use('../styles/black.mplstyle')
plt.rc('xtick.major', size=0)
plt.rc('ytick.major', size=0)


# Initialize a dictionary to contain the data to plot
counts = {}
for mission in MISSIONS:
    counts[mission] = {}
    for year in range(first_year, current_year + 1):
        counts[mission][year] = 0

    cur = db.con.execute("SELECT year, COUNT(*) FROM pubs "
                      "WHERE mission = ? "
                      "AND year >= '2014' "
                      "GROUP BY year;",
                      [mission])
    rows = list(cur.fetchall())
    for row in rows:
        counts[mission][int(row[0])] = row[1]

# Now make the actual plot
fig = plt.figure(figsize=(8, 4.5))
ax = fig.add_subplot(111)
plt.bar(np.array(list(counts['k2'].keys())) - 0.5*barwidth,
        counts['k2'].values(),
        label='K2',
        facecolor=palette[0],
        edgecolor='black',
        width=barwidth)
# Also plot the extrapolated precition for the current year
if extrapolate:
    now = datetime.datetime.now()
    fraction_of_year_passed = float(now.strftime("%-j")) / 365.2425
    current_total = (counts['k2'][current_year])
    expected = (1/fraction_of_year_passed - 1) * current_total
    plt.bar(current_year - 0.5*barwidth,
            expected,
            bottom=current_total,
            label='Extrapolation',
            facecolor='#34495e',
            edgecolor='black',
            width=barwidth)

# Aesthetics
plt.ylabel("Publications per year", fontsize=18)
ax.get_xaxis().get_major_formatter().set_useOffset(False)
plt.xticks(range(first_year - 1, current_year + 1), fontsize=18)
plt.yticks(range(0, 151, 50), fontsize=18)
plt.xlim([first_year - 0.75*barwidth, current_year + 0.75*barwidth])
"""
plt.legend(bbox_to_anchor=(0.1, 1),
           loc='upper left',
           ncol=3,
           borderaxespad=0.,
           handlelength=0.8,
           frameon=False,
           fontsize=18)
"""
# Disable spines
ax.spines["left"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["top"].set_visible(False)
ax.spines["bottom"].set_visible(False)
# Only show bottom and left ticks
ax.get_xaxis().tick_bottom()
ax.get_yaxis().tick_left()
# Only show horizontal grid lines
ax.grid(axis='y')

n_pub = sum(counts['k2'].values())
plt.suptitle("K2 Contributed to "
             "{} Publications So Far".format(n_pub),
             fontsize=22)

plt.tight_layout(rect=(0, 0, 1, 0.92), h_pad=1.5)
log.info("Writing {}".format(output_fn))
plt.savefig(output_fn)
plt.close()

