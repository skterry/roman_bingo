"""Streamlit app: Roman Galactic Bulge BINGO"""

import io
import os
import random
from itertools import groupby

import matplotlib
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

try:
    import smplotlib
except ImportError:
    pass

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

RANGES = {
    'R': range(1, 19),
    'O': range(19, 37),
    'M': range(37, 55),
    'A': range(55, 73),
    'N': range(73, 91),
}


def letter_for(n):
    for letter, r in RANGES.items():
        if n in r:
            return letter


def generate_bingo_sheet():
    """Return (pdf_bytes, png_bytes) for a new randomized bingo sheet."""
    with plt.style.context('classic'):
        matplotlib.rcParams.update({
            "font.size": 16,
            "axes.linewidth": 3,
            'xtick.major.size': 10, 'xtick.major.width': 2,
            'xtick.minor.size': 5,  'xtick.minor.width': 2,
            'ytick.major.size': 10, 'ytick.major.width': 2,
            'ytick.minor.size': 5,  'ytick.minor.width': 2,
        })

        fig = plt.figure(figsize=(11, 8.5))
        ax = fig.add_axes([0.10, 0.12, 0.87, 0.76])

        layout = 'layout_7f_3'
        fields = []
        with open(os.path.join(SCRIPT_DIR, 'ref_files', f'{layout}.outline.lbad')) as fp:
            for k, g in groupby(fp, lambda x: x.startswith(' ')):
                if not k:
                    fields.append(
                        np.array([[float(x) for x in d.split()] for d in g if d.strip()])
                    )

        for f in fields:
            ax.plot(f[:, 1] - 0.15, f[:, 2] + 0.23, 'k-', lw=2.5, alpha=1, zorder=1000)

        fields_sorted = sorted(fields, key=lambda f: -np.mean(f[:, 1] - 0.15))
        for letter, f in zip('ROMAN', fields_sorted):
            cx = np.mean(f[:, 1] - 0.15)
            top_y = np.max(f[:, 2] + 0.23)
            ax.text(cx, top_y + 0.05, letter, ha='center', va='bottom',
                    fontsize=22, fontweight='bold', zorder=1001)

        f0 = fields_sorted[0]
        fy = f0[:, 2] + 0.23
        ax_pos = ax.get_position()
        x_scale = (ax_pos.width  * fig.get_figwidth())  / 2.8
        y_scale = (ax_pos.height * fig.get_figheight()) / 2.4
        cell_h = (fy.max() - fy.min()) / 6 * 0.94
        cell_w = cell_h * (y_scale / x_scale)

        all_centers = {
            'R': [(1.41,  -1.744), (1.255, -1.744), (1.12,  -1.744),
                  (1.36,  -1.610), (1.205, -1.610), (1.07,  -1.610),
                  (1.33,  -1.477), (1.175, -1.477), (1.04,  -1.477),
                  (1.33,  -1.342), (1.175, -1.342), (1.04,  -1.342),
                  (1.36,  -1.209), (1.205, -1.209), (1.07,  -1.209),
                  (1.41,  -1.075), (1.255, -1.075), (1.12,  -1.075)],
            'O': [(1.001026, -1.744), (0.846026, -1.744), (0.711026, -1.744),
                  (0.951026, -1.610), (0.796026, -1.610), (0.661026, -1.610),
                  (0.921026, -1.477), (0.766026, -1.477), (0.631026, -1.477),
                  (0.921026, -1.342), (0.766026, -1.342), (0.631026, -1.342),
                  (0.951026, -1.209), (0.796026, -1.209), (0.661026, -1.209),
                  (1.001026, -1.075), (0.846026, -1.075), (0.711026, -1.075)],
            'M': [(0.592052, -1.744), (0.437052, -1.744), (0.302052, -1.744),
                  (0.542052, -1.610), (0.387052, -1.610), (0.252052, -1.610),
                  (0.512052, -1.477), (0.357052, -1.477), (0.222052, -1.477),
                  (0.512052, -1.342), (0.357052, -1.342), (0.222052, -1.342),
                  (0.542052, -1.209), (0.387052, -1.209), (0.252052, -1.209),
                  (0.592052, -1.075), (0.437052, -1.075), (0.302052, -1.075)],
            'A': [( 0.183078, -1.744), ( 0.028078, -1.744), (-0.106922, -1.744),
                  ( 0.133078, -1.610), (-0.021922, -1.610), (-0.156922, -1.610),
                  ( 0.103078, -1.477), (-0.051922, -1.477), (-0.186922, -1.477),
                  ( 0.103078, -1.342), (-0.051922, -1.342), (-0.186922, -1.342),
                  ( 0.133078, -1.209), (-0.021922, -1.209), (-0.156922, -1.209),
                  ( 0.183078, -1.075), ( 0.028078, -1.075), (-0.106922, -1.075)],
            'N': [(-0.225896, -1.744), (-0.380896, -1.744), (-0.515896, -1.744),
                  (-0.275896, -1.610), (-0.430896, -1.610), (-0.565896, -1.610),
                  (-0.305896, -1.477), (-0.460896, -1.477), (-0.595896, -1.477),
                  (-0.305896, -1.342), (-0.460896, -1.342), (-0.595896, -1.342),
                  (-0.275896, -1.209), (-0.430896, -1.209), (-0.565896, -1.209),
                  (-0.225896, -1.075), (-0.380896, -1.075), (-0.515896, -1.075)],
        }
        offsets = {'R': 1, 'O': 19, 'M': 37, 'A': 55, 'N': 73}

        def draw_column(centers, offset, selected):
            for i, (cx, cy) in enumerate(centers):
                alpha = 1.0 if i in selected else 0.05
                ax.add_patch(patches.Rectangle(
                    (cx - 0.5 * cell_w, cy - 0.5 * cell_h), cell_w, cell_h,
                    linewidth=1.5, edgecolor='black', facecolor='white',
                    alpha=alpha, zorder=997 + (1 if i in selected else 0),
                ))
                if i in selected:
                    ax.text(cx, cy, str(i + offset), ha='center', va='center',
                            fontsize=10, zorder=999)

        for letter in 'ROMAN':
            selected = set(random.sample(range(18), 5))
            draw_column(all_centers[letter], offsets[letter], selected)

        gcfields = []
        with open(os.path.join(SCRIPT_DIR, 'ref_files', f'{layout}.outline.gc.lbad')) as fp:
            for k, g in groupby(fp, lambda x: x.startswith(' ')):
                if not k:
                    gcfields.append(
                        np.array([[float(x) for x in d.split()] for d in g if d.strip()])
                    )
        for f in gcfields:
            ax.plot(f[:, 1] + 0.055, f[:, 2] - 0.18, 'k', lw=2.5, alpha=0.1, zorder=1000)

        ax.set_xlim([1.8, -1.0])
        ax.set_ylim([-2.3, 0.1])
        ax.set_xlabel(r'$\ell$ $[$deg$]$', fontsize=18)
        ax.set_ylabel(r'$b$ $[$deg$]$', fontsize=18)
        ax.text(0.45, -0.1, 'Galactic Bulge BINGO', ha='center', va='center',
                fontsize=40, fontweight='bold', zorder=1001)
        ax.text(-0.9, -2.2, 'Created by: S. K. Terry', ha='right', va='bottom',
                fontsize=9, alpha=0.1, zorder=1001)

        pdf_buf = io.BytesIO()
        plt.savefig(pdf_buf, format='pdf')
        pdf_buf.seek(0)

        png_buf = io.BytesIO()
        plt.savefig(png_buf, format='png', dpi=120)
        png_buf.seek(0)

        plt.close(fig)

    return pdf_buf.getvalue(), png_buf.getvalue()


def main():
    st.set_page_config(
        page_title="Roman Galactic Bulge BINGO",
        page_icon=os.path.join(SCRIPT_DIR, "ref_files", "RST_icon.png"),
        layout="wide",
    )
    st.title("Roman Galactic Bulge BINGO")

    tab_sheet, tab_caller = st.tabs(["Bingo Sheet", "Number Caller"])

    # ── Sheet Generator ───────────────────────────────────────────────────────
    with tab_sheet:
        st.subheader("Generate a Personalised Bingo Sheet")
        st.write(
            "Each sheet shows 5 randomly selected detector chips per field (R, O, M, A, N). "
            "Download the PDF, print it (optional), and you're ready to play."
        )

        if st.button("Generate New Sheet", type="primary"):
            with st.spinner("Generating…"):
                pdf_bytes, png_bytes = generate_bingo_sheet()
                st.session_state.pdf_bytes = pdf_bytes
                st.session_state.png_bytes = png_bytes

        if 'png_bytes' in st.session_state:
            st.image(st.session_state.png_bytes, width='stretch')
            st.download_button(
                label="Download PDF",
                data=st.session_state.pdf_bytes,
                file_name="roman_bingo_sheet.pdf",
                mime="application/pdf",
            )

    # ── Number Caller ─────────────────────────────────────────────────────────
    with tab_caller:
        st.subheader("ROMAN BINGO — Number Caller")

        for key, default in [
            ('game_pool',   []),
            ('game_called', []),
            ('game_active', False),
            ('last_called', None),
        ]:
            if key not in st.session_state:
                st.session_state[key] = default

        ctrl_col, board_col = st.columns([1, 2])

        with ctrl_col:
            if st.button("Start / Reset Game", type="primary"):
                pool = list(range(1, 91))
                random.shuffle(pool)
                st.session_state.game_pool   = pool
                st.session_state.game_called = []
                st.session_state.game_active = True
                st.session_state.last_called = None

            if st.session_state.game_active:
                st.divider()
                pool_empty = len(st.session_state.game_pool) == 0

                if st.button("Draw Next Number", disabled=pool_empty):
                    if st.session_state.game_pool:
                        n = st.session_state.game_pool.pop()
                        letter = letter_for(n)
                        st.session_state.game_called.append((letter, n))
                        st.session_state.last_called = (letter, n)
                    else:
                        st.error("All numbers have been drawn, please start a new game.")

                n_called = len(st.session_state.game_called)
                st.metric("Called", f"{n_called} / 90")

                if st.session_state.last_called:
                    l, n = st.session_state.last_called
                    st.markdown("**Last drawn:**")
                    st.markdown(
                        f"<h1 style='color:#cc0000;'>{l} &ndash; {n}</h1>",
                        unsafe_allow_html=True,
                    )

                if pool_empty:
                    st.success("All 90 numbers have been called!")

        with board_col:
            if st.session_state.game_active and st.session_state.game_called:
                st.markdown("**Numbers called by column**")
                called = st.session_state.game_called
                last   = st.session_state.last_called

                cols = st.columns(5)
                for i, letter in enumerate('ROMAN'):
                    with cols[i]:
                        rng  = RANGES[letter]
                        nums = [n for (l, n) in called if l == letter]
                        st.markdown(
                            f"<p style='font-size:2.5rem; font-weight:bold; margin:0'>"
                            f"{letter} <span style='font-size:1rem; font-weight:normal'>({rng.start}–{rng.stop - 1})</span></p>",
                            unsafe_allow_html=True,
                        )
                        for n in nums:
                            if last and last == (letter, n):
                                st.markdown(
                                    f"<p style='font-size:2.5rem; color:#cc0000; font-weight:bold; margin:2px 0'>{n}</p>",
                                    unsafe_allow_html=True,
                                )
                            else:
                                st.markdown(
                                    f"<p style='font-size:2.5rem; margin:2px 0'>{n}</p>",
                                    unsafe_allow_html=True,
                                )


if __name__ == '__main__':
    main()
