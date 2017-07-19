import matplotlib.pyplot as pl
from matplotlib.ticker import MultipleLocator
from matplotlib import style

import seaborn as sns
import pandas as pd

OUTPUT_PREFIX = 'kepler-k2-host-star-brightness'
OUTPUT_SUFFIX = '.png'

palette = sns.color_palette(['#f1c40f', '#2980b9'])
style.use('../styles/black.mplstyle')

kepler_df = pd.read_csv('../data/kepler-confirmed-planets.csv')
k2_df = pd.read_csv('../data/k2-confirmed-planets.csv')

xlim = [8, 20]

pl.figure(figsize=(8, 4.5))
pl.hist(k2_df.st_optmag, histtype="step", normed=True, bins=30, range=xlim, lw=3,
        label="K2", edgecolor=palette[0])
pl.hist(kepler_df.st_optmag, histtype="step", normed=True, bins=31, range=xlim, lw=5,
        label="Kepler", edgecolor="#2980b9", zorder=-1)
pl.legend(bbox_to_anchor=(0., 1., 1., 0.),
          loc=8,
          ncol=2,
          borderaxespad=0.,
          handlelength=0.8,
          frameon=False,
          scatterpoints=3)
pl.axes().xaxis.set_major_locator(MultipleLocator(1))
pl.yticks([])
pl.xlabel("Host star brightness (V)")
pl.xlim(xlim)
pl.tight_layout(rect=(0, 0, 1, 0.92))
#pl.show()
output_fn = OUTPUT_PREFIX + OUTPUT_SUFFIX
print('Writing {}'.format(output_fn))
pl.savefig(output_fn, dpi=200)
