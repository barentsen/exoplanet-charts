import matplotlib.pyplot as pl
from matplotlib.ticker import MultipleLocator
from matplotlib import style

import seaborn as sns
import pandas as pd

SHOW_KEPLER = False #True
K_MAGNITUDE_CUT = 11
OUTPUT_PREFIX = 'k2-planets-for-atmospheric-characterization'
OUTPUT_SUFFIX = '.png'

if SHOW_KEPLER:
    OUTPUT_PREFIX += '-with-kepler'

palette = sns.color_palette(['#f1c40f', '#2980b9'])
style.use('../styles/black.mplstyle')

k2_df = pd.read_csv('../data/k2-candidate-planets.csv')
k2_df = k2_df[k2_df.st_k2 <= K_MAGNITUDE_CUT]

print('Plotting {} points.'.format(len(k2_df)))

fig = pl.figure(figsize=(8, 4.5))
pl.fill_between([.5, .5, 2.5, 2.5, .5],
                [2000, 4000, 4000, 2000, 2000],
                zorder=-1, alpha=0.3,
                facecolor=palette[1],
                lw=0)
pl.plot([.5, .5, 2.5, 2.5, .5],
                [2000, 4000, 4000, 2000, 2000],
                zorder=-1, alpha=1,
                color='white',
                lw=1.5, linestyle='dotted',
                dashes=[2, 4])
pl.scatter(k2_df.pl_rade, k2_df.st_teff,
           lw=0.4, s=35, label='K2',
           facecolor=palette[0], edgecolor='black',
           zorder=30)

if SHOW_KEPLER:
    kepler_df = pd.read_csv('../data/kepler-candidate-planets.csv')
    kepler_df = kepler_df[kepler_df.koi_kmag <= K_MAGNITUDE_CUT]
    pl.scatter(kepler_df.koi_prad, kepler_df.koi_steff,
               lw=0.4, s=35,
               label='Kepler',
               facecolor='#2980b9',
               edgecolor='black',
               zorder=20)

pl.legend(bbox_to_anchor=(0., 1., 1., 0.),
          loc=8,
          ncol=2,
          borderaxespad=0.,
          handlelength=0.8,
          frameon=False,
          scatterpoints=3)

# Annotations
pl.annotate("Earth and Super Earth-size Candidates\n"
            "Orbiting Cool Dwarfs",
            style='italic',
            xy=(2.5, 2900), xycoords='data',
            xytext=(2.8, 2900), textcoords='data',
            va="center", size=12,
            arrowprops=dict(arrowstyle="-", lw=1)
            )
pl.suptitle("Planet Candidates for Atmospheric Characterization (Ks < 11)")

# Axes
pl.yticks([3000, 4000, 5000, 6000, 7000],
          ['3,000 K', '4,000 K', '5,000 K', '6,000 K', '7,000 K'])
pl.axes().xaxis.set_minor_locator(MultipleLocator(0.5))
pl.axes().yaxis.set_minor_locator(MultipleLocator(500))
pl.xlim(0.0, 5)
pl.ylim(2250, 7000)
pl.xlabel('Planet Size Relative to Earth (Radius)')
pl.ylabel('Host Star Temperature')

pl.tight_layout(rect=(0, 0, 1, 0.92))
output_fn = OUTPUT_PREFIX + OUTPUT_SUFFIX
print('Writing {}'.format(output_fn))
pl.savefig(output_fn, dpi=200)
pl.close()
