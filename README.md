# Roman Galactic Bulge BINGO

A bingo game themed around the Nancy Grace Roman Space Telescope Galactic Bulge Time Domain Survey. Each column of the bingo card (**R**, **O**, **M**, **A**, **N**) corresponds to one of five survey fields, and each number represents a detector chip within that field (1–90 total across all five fields). The 6th Galactic Center (GC) field is ignored in this game.

## Project Structure

| File | Description |
|------|-------------|
| `app.py` | Main Streamlit web application |
| `roman_bingo.py` | Standalone script to generate a bingo sheet PDF |
| `bingo_caller.py` | Standalone terminal-based bingo number caller |
| `layout_7f_3.outline.lbad` | Survey field outline coordinates |
| `layout_7f_3.outline.gc.lbad` | Galactic center region outline coordinates |
| `RST_icon.png` | Browser tab icon used by the Streamlit app |

## Playing Roman Bingo Online

The game is hosted online and can be played at the following URL:

```bash
https://romanbingo.streamlit.app/
```

## Running the Streamlit App Locally

Run the following to launch the streamlit app in your local browser:

```bash
streamlit run app.py
```

The app has two tabs:

- **Bingo Sheet** — Generates a randomized card with 5 randomly selected detector chips per field. Preview it in the browser and download as a print-ready PDF.
- **Number Caller** — Interactive caller that draws numbers one at a time from a shuffled pool of 1–90, displaying all called numbers organized by field column (R / O / M / A / N).

## Standalone Scripts

Generate a bingo sheet without Streamlit (file saved as `bingo_sheet.pdf`):

```bash
python roman_bingo.py
```

Run the terminal-based number caller:

```bash
python bingo_caller.py
```

Press **Enter** to draw the next number; type **q** to end the game.

## Dependencies

Core packages:

- `numpy`
- `matplotlib`
- `scipy`
- `astropy`

Install Streamlit if not already present:

```bash
pip install streamlit
```
