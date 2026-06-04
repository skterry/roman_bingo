import argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from itertools import groupby

import matplotlib.font_manager as fm
import matplotlib.patheffects as PathEffects
import matplotlib.patches as patches
from matplotlib import ticker
from scipy.interpolate import griddata
import sys
import os

import pandas as pd

import matplotlib
if float(matplotlib.__version__[0:3])>=2:
    plt.style.use('classic')

from astropy import units as u
from astropy.coordinates import SkyCoord
from matplotlib.backends.backend_pdf import PdfPages

import pdb
try:
    import smplotlib
except ImportError:
    pass
import random


parser = argparse.ArgumentParser(description='Generate Roman Bingo sheets')
parser.add_argument('-n', type=int, default=1,
                    help='Number of randomized bingo sheets to generate (default: 1)')
args = parser.parse_args()


layout = 'layout_7f_3'

plotchips = 0
plotcenters = 0
plotoutlines = 1

plt.rcParams["font.size"] = 16
plt.rcParams["axes.linewidth"] = 3
plt.rcParams['xtick.major.size'] = 10
plt.rcParams['xtick.major.width'] = 2
plt.rcParams['xtick.minor.size'] = 5
plt.rcParams['xtick.minor.width'] = 2
plt.rcParams['ytick.major.size'] = 10
plt.rcParams['ytick.major.width'] = 2
plt.rcParams['ytick.minor.size'] = 5
plt.rcParams['ytick.minor.width'] = 2


# Read outline files once so they aren't re-parsed for every sheet.
fields = []
gcfields = []
if plotoutlines == 1:
    with open('ref_files/%s.outline.lbad' % layout) as fp:
        for k, g in groupby(fp, lambda x: x.startswith(' ')):
            if not k:
                fields.append(np.array([[float(x) for x in d.split()] for d in g if len(d.strip())]))

    with open('ref_files/%s.outline.gc.lbad' % layout) as fp:
        for k, g in groupby(fp, lambda x: x.startswith(' ')):
            if not k:
                gcfields.append(np.array([[float(x) for x in d.split()] for d in g if len(d.strip())]))


def draw_field_squares(ax, centers, offset, selected, cell_w, cell_h):
    """Draw 18 squares: faint for unselected, solid with number for selected."""
    for i in range(18):
        cx, cy = centers[i]
        if i in selected:
            rect = patches.Rectangle(
                (cx - 0.5*cell_w, cy - 0.5*cell_h), cell_w, cell_h,
                linewidth=1.5, edgecolor='black', facecolor='white',
                alpha=1.0, zorder=998)
            ax.add_patch(rect)
            ax.text(cx, cy, str(i + offset), ha='center', va='center',
                    fontsize=10, zorder=999)
        else:
            rect = patches.Rectangle(
                (cx - 0.5*cell_w, cy - 0.5*cell_h), cell_w, cell_h,
                linewidth=1.5, edgecolor='black', facecolor='white',
                alpha=0.05, zorder=997)
            ax.add_patch(rect)


square_centers = [
    (1.41,-1.744), (1.255,-1.744), (1.12,-1.744),
    (1.36,-1.610), (1.205,-1.610), (1.07,-1.610),
    (1.33,-1.477), (1.175,-1.477), (1.04,-1.477),
    (1.33,-1.342), (1.175,-1.342), (1.04,-1.342),
    (1.36,-1.209), (1.205,-1.209), (1.07,-1.209),
    (1.41,-1.075), (1.255,-1.075), (1.12,-1.075),
]
square_centers_O = [
    (1.001026,-1.744), (0.846026,-1.744), (0.711026,-1.744),
    (0.951026,-1.610), (0.796026,-1.610), (0.661026,-1.610),
    (0.921026,-1.477), (0.766026,-1.477), (0.631026,-1.477),
    (0.921026,-1.342), (0.766026,-1.342), (0.631026,-1.342),
    (0.951026,-1.209), (0.796026,-1.209), (0.661026,-1.209),
    (1.001026,-1.075), (0.846026,-1.075), (0.711026,-1.075),
]
square_centers_M = [
    (0.592052,-1.744), (0.437052,-1.744), (0.302052,-1.744),
    (0.542052,-1.610), (0.387052,-1.610), (0.252052,-1.610),
    (0.512052,-1.477), (0.357052,-1.477), (0.222052,-1.477),
    (0.512052,-1.342), (0.357052,-1.342), (0.222052,-1.342),
    (0.542052,-1.209), (0.387052,-1.209), (0.252052,-1.209),
    (0.592052,-1.075), (0.437052,-1.075), (0.302052,-1.075),
]
square_centers_A = [
    ( 0.183078,-1.744), ( 0.028078,-1.744), (-0.106922,-1.744),
    ( 0.133078,-1.610), (-0.021922,-1.610), (-0.156922,-1.610),
    ( 0.103078,-1.477), (-0.051922,-1.477), (-0.186922,-1.477),
    ( 0.103078,-1.342), (-0.051922,-1.342), (-0.186922,-1.342),
    ( 0.133078,-1.209), (-0.021922,-1.209), (-0.156922,-1.209),
    ( 0.183078,-1.075), ( 0.028078,-1.075), (-0.106922,-1.075),
]
square_centers_N = [
    (-0.225896,-1.744), (-0.380896,-1.744), (-0.515896,-1.744),
    (-0.275896,-1.610), (-0.430896,-1.610), (-0.565896,-1.610),
    (-0.305896,-1.477), (-0.460896,-1.477), (-0.595896,-1.477),
    (-0.305896,-1.342), (-0.460896,-1.342), (-0.595896,-1.342),
    (-0.275896,-1.209), (-0.430896,-1.209), (-0.565896,-1.209),
    (-0.225896,-1.075), (-0.380896,-1.075), (-0.515896,-1.075),
]


out_file = 'bingo_sheet.pdf' if args.n == 1 else 'bingo_sheets.pdf'

with PdfPages(out_file) as pdf:
    for sheet_idx in range(args.n):
        fig = plt.figure(figsize=(8.5, 11))
        ax2 = fig.add_axes([0.0, 0.20, 1.00, 0.60])

        if plotoutlines == 1:
            for f in fields:
                ax2.plot(f[:,1]-0.15, f[:,2]+0.23, 'k-', lw=2.5, alpha=1, zorder=1000)

            letters = ['R', 'O', 'M', 'A', 'N']
            fields_sorted = sorted(fields, key=lambda f: -np.mean(f[:,1] - 0.15))
            for letter, f in zip(letters, fields_sorted):
                cx = np.mean(f[:,1] - 0.15)
                top_y = np.max(f[:,2] + 0.23)
                ax2.text(cx, top_y + 0.05, letter, ha='center', va='bottom',
                         fontsize=22, fontweight='bold', zorder=1001)

            f0 = fields_sorted[0]
            fx = f0[:,1] - 0.15
            fy = f0[:,2] + 0.23
            ymin0, ymax0 = fy.min(), fy.max()
            ncols, nrows = 3, 6

            fig_w_in, fig_h_in = fig.get_size_inches()
            ax_pos = ax2.get_position()
            x_scale = (ax_pos.width  * fig_w_in) / 2.8
            y_scale = (ax_pos.height * fig_h_in) / 2.4

            shrink = 0.94
            cell_h = (ymax0 - ymin0) / nrows * shrink
            cell_w = cell_h * (y_scale / x_scale)

            draw_field_squares(ax2, square_centers,   1,  set(random.sample(range(18), 5)), cell_w, cell_h)
            draw_field_squares(ax2, square_centers_O, 19, set(random.sample(range(18), 5)), cell_w, cell_h)
            draw_field_squares(ax2, square_centers_M, 37, set(random.sample(range(18), 5)), cell_w, cell_h)
            draw_field_squares(ax2, square_centers_A, 55, set(random.sample(range(18), 5)), cell_w, cell_h)
            draw_field_squares(ax2, square_centers_N, 73, set(random.sample(range(18), 5)), cell_w, cell_h)

        if plotoutlines == 1:
            for f in gcfields:
                ax2.plot(f[:,1]+0.055, f[:,2]-0.18, 'k', lw=2.5, alpha=0.1, zorder=1000)

        ax2.set_xlim([1.8, -1.0])
        ax2.set_ylim([-2.3, 0.1])
        ax2.set_xlabel(r'$\ell$ $[$deg$]$', fontsize=18)
        ax2.set_ylabel(r'$b$ $[$deg$]$', fontsize=18)

        ax2.text(0.45, -0.1, 'Galactic Bulge BINGO', ha='center', va='center',
                 fontsize=40, fontweight='bold', zorder=1001)
        ax2.text(-0.9, -2.2, 'Created by: S. K. Terry', ha='right', va='bottom',
                 fontsize=9, alpha=0.3, zorder=1001)

        pdf.savefig(fig)
        plt.close(fig)

print('Saved %d sheet(s) to %s' % (args.n, out_file))
