"""
Start of Kepler observations: 2009 May 2
First Kepler release: 2010 Jun 15

Start of K2 observation (C0): 2014 Mar 8
First release of K2 data: 2014 Sep 08

=> Limit to 2 years after start of data taking,
i.e. 2016 Mar for K2 and 2011 May for Kepler.
"""
import matplotlib as mpl
import matplotlib.pyplot as pl
from matplotlib.ticker import MultipleLocator
from matplotlib import style

import seaborn as sns
import numpy as np
import pandas as pd

OUTPUT_PREFIX = 'kepler-author-seniority'
OUTPUT_SUFFIX = '.png'
BINS = [0, 4.5, 10.5, 19.5, 100]  # years

palette = sns.color_palette(['#f1c40f', '#2980b9'])
style.use('../styles/black.mplstyle')
pl.rc('ytick.major', size=0)
pl.rc('xtick.major', size=0)

k = pd.read_excel('data/lead-authors-in-first-two-years-of-kepler.xls')
k2 = pd.read_excel('data/lead-authors-in-first-two-years-of-k2.xls')

k_seniority = k['year'] - k['year_of_first_paper']
k2_seniority = k2['year'] - k2['year_of_first_paper']
print('Median seniority\n'
      'Kepler: {} yrs\n'
      'K2: {} yrs'.format(np.median(k_seniority), np.median(k2_seniority)))


def binning(data, bins):
    return np.histogram(data, bins=bins)[0]


fig = pl.figure()
pl.subplots_adjust(left=0.12, right=0.98,
                    bottom=0.15, top=0.98,
                    hspace=0.2)

ax_k = pl.subplot(111)
ax_k.bar(left=np.array(range(len(BINS)-1)) + 0.1 + 0.6,
         height=binning(k2_seniority, BINS),
         color=palette[0], edgecolor='black',
         alpha=0.8, width=0.6, zorder=20,
         label='K2 (first two years)')
ax_k.bar(left=np.array(range(len(BINS)-1)) + 0.6,
         height=binning(k_seniority, BINS),
         color="#2980b9", edgecolor='black',
         alpha=0.8, width=0.8, zorder=10,
         label='Kepler (first two years)')

# Disable spines
ax_k.spines["left"].set_visible(False)
ax_k.spines["right"].set_visible(False)
ax_k.spines["top"].set_visible(False)
ax_k.spines["bottom"].set_visible(False)

# Only show bottom and left ticks
ax_k.get_xaxis().tick_bottom()
ax_k.get_yaxis().tick_left()
pl.grid(axis='x')
pl.yticks([0, 10, 20, 30], fontsize=18)
pl.xticks([1, 2, 3, 4],
          ['0-5 yrs', '5-10 yrs', '10-20 yrs', '20+ yrs'],
          fontsize=18)

ax_k.set_xlabel('Seniority of lead author (years since first paper)',
                fontsize=18)
ax_k.set_ylabel("Exoplanet papers", fontsize=18)
pl.suptitle("K2's Open Data Policy Empowers Early-Career Astronomers", fontsize=22)

pl.legend(bbox_to_anchor=(1, 0.95),
          ncol=1,
          borderaxespad=0.,
          handlelength=0.8,
          frameon=False,
          fontsize=16)

pl.tight_layout(rect=(0, 0, 1, 0.92))

output_fn = OUTPUT_PREFIX + OUTPUT_SUFFIX
print('Writing {}'.format(output_fn))
pl.savefig(output_fn, dpi=200)
pl.close()

# Print some stats
k_surnames = k.lead_author.str.split(pat=',', expand=True)[0]
k2_surnames = k2.lead_author.str.split(pat=',', expand=True)[0]
print("Papers: Kepler {}, K2 {}".format(len(k), len(k2)))
print("Unique authors: Kepler {}, K2 {}".format(
    k_surnames.unique().size,
    k2_surnames.unique().size))
print("Unique institutions: Kepler {}, K2 {}".format(
    k.affiliation.unique().size,
    k2.affiliation.unique().size))
