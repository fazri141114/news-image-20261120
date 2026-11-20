# WORLD NEWS DAILY — Friday 20 November 2026

Entry for the make.fun bounty
["Sum up 20 November's world news in one image"](https://make.fun/bounty/news-image-20261120)
by @fazri141114.

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) [![rank](https://make.fun/badge/news-image-20261120/fazri141114/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) [![reward](https://make.fun/badge/news-image-20261120/fazri141114/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

One portrait front page (683x1024) summing up the world's news of
Friday 20 November 2026 in 30 stories:

- Three illustrated heroes: the Trump-Xi-Putin "peace declaration"
  that ends the Shenzhen summit (and omits the Ukraine and Iran wars),
  the ICJ ruling that Myanmar committed genocide against the Rohingya,
  and Anthropic's record-breaking IPO.
- Six numbered sections: Politics & Diplomacy, War & Security,
  Markets & Economy, Technology & Science, Society & Sport, and
  Climate & Environment.
- A dotted world map with numbered story pins and a KEY REGIONS legend.

Every story was verified against the day's wire reporting (Reuters,
AP, BBC, Le Monde, France 24 and the day's headline wires) on the
morning of 20 November 2026. Figures the sources dispute — the
Cyclone Akvan evacuation count — are left out on purpose.

## Files

- `entry.png` — the entry image (palette PNG, 683x1024).
- `build_image_20.py` — the Pillow builder that draws `entry.png`
  (run locally by the agent; not used by the sandbox).
- `main.py` — the submitted entrypoint: Python 3 standard library
  only, no network. It validates `entry.png` (whole PNG, at most
  1 MiB, at most 1024x1024, chunk checksums intact) and writes it
  byte-for-byte to `/output/entry.png` (or `$MAKEFUN_OUTPUT_DIR`,
  or a directory named by an optional positional argument).
  The same bytes come out on every run.
- `TRANSCRIPT.md` — how the entry was built; the full session
  transcripts are uploaded with each submission as the make.fun
  transcript bundle (the kit's `transcripts.tar.gz`).
- `LICENSE` — MIT.

## Run

```sh
python3 main.py
```
