import matplotlib.pyplot as pl
from matplotlib.ticker import MultipleLocator
from matplotlib import style

import seaborn as sns
import pandas as pd

palette = sns.color_palette(['#f1c40f', '#2980b9'])
style.use('../styles/black.mplstyle')

K_MAGNITUDE_CUT = 11
k2_df = pd.read_csv('../data/k2-planets.csv')
k2_df = k2_df[k2_df.st_k2 <= K_MAGNITUDE_CUT]

print('Plotting {} points.'.format(len(k2_df)))

fig = pl.figure()
pl.fill_between([.5, .5, 2.5, 2.5, .5],
                [2000, 4000, 4000, 2000, 2000],
                lw=0, zorder=-1, alpha=0.3,
                facecolor=palette[1], edgecolor=palette[1])
pl.scatter(k2_df.pl_rade, k2_df.st_teff, lw=0.4, s=35, label='K2',
           facecolor=palette[0], edgecolor='black')

# Annotations
pl.annotate("Earth and Super Earth-size Candidates\n"
            "Orbiting Cool Dwarfs",
            xy=(2.5, 2900), xycoords='data',
            xytext=(2.8, 2900), textcoords='data',
            va="center", size=12,
            arrowprops=dict(arrowstyle="-")
            )
pl.suptitle("K2 Planet Candidates for Atmospheric Characterization (Ks < 11)")

# Axes
pl.yticks([3000, 4000, 5000, 6000, 7000],
          ['3,000 K', '4,000 K', '5,000 K', '6,000 K', '7,000 K'])
pl.axes().xaxis.set_minor_locator(MultipleLocator(0.2))
pl.axes().yaxis.set_minor_locator(MultipleLocator(200))
pl.xlim(0.0, 5)
pl.ylim(2250, 7000)
pl.xlabel('Planet Size Relative to Earth (Radius)')
pl.ylabel('Host Star Temperature')

pl.tight_layout(rect=(0, 0, 1, 0.92))
pl.savefig("k2-planets-for-atmospheric-characterization.png", dpi=200)
pl.close()
