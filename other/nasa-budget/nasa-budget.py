"""Creates beautiful visualizations of the publication database."""
import json
import numpy as np

from matplotlib import pyplot as plt
import matplotlib.patheffects as path_effects
import matplotlib as mpl
from matplotlib import style
import seaborn as sns

from kpub import PublicationDB

output_fn = 'nasa-budget.png'

palette = sns.color_palette(['#f1c40f', '#2980b9'])
style.use('../styles/black.mplstyle')
plt.rc('xtick.major', size=0)
plt.rc('ytick.major', size=0)


with open('nasa_budget.json', 'r') as data_file:
    data = json.load(data_file)


# Now make the actual plot
fig = plt.figure() #figsize=(8, 4.5))
ax = fig.add_subplot(111)

plt.bar(data['year'], data['perc_budget'],
        facecolor=palette[1],
        edgecolor='black',
        width=1)


# Aesthetics
plt.ylabel("%", fontsize=18)
plt.xlabel("Year", fontsize=18)

ax.get_xaxis().get_major_formatter().set_useOffset(False)
plt.xticks([1960, 1970, 1980, 1990, 2000, 2010], fontsize=18)
plt.yticks([0, 1, 2, 3, 4], fontsize=18)
plt.xlim([1958, 2013])
plt.legend(bbox_to_anchor=(0.1, 1),
           loc='upper left',
           ncol=3,
           borderaxespad=0.,
           handlelength=0.8,
           frameon=False,
           fontsize=18)
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

plt.suptitle("NASA Budget as a Percentage of the US Federal Budget",
             fontsize=22)

plt.tight_layout(rect=(0, 0, 1, 0.92), h_pad=1.5)
print('Writing {}'.format(output_fn))
plt.savefig(output_fn)
plt.close()

