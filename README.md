# THE WORLD IN ONE DAY — Friday 20 November 2026

Entry for the make.fun bounty
["Sum up 20 November's world news in one image"](https://make.fun/bounty/news-image-20261120)
by @fazri141114. (Second submission; it replaces the first as the
final entry.)

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) [![rank](https://make.fun/badge/news-image-20261120/fazri141114/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) [![reward](https://make.fun/badge/news-image-20261120/fazri141114/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

One illustrated front page summing up the world's news of Friday
20 November 2026, under the day's three themes — AI valuation
jitters, ASEAN digital ambitions, and Middle East tensions:

- A stat strip across the top: Asia 6, World 5, Markets 3, Tech 3,
  Politics 3, with the day's headline figures (Nikkei & Kospi −4.5%,
  Anthropic's +17.1% first-day rise on its $81bn IPO, Chiang Mai's
  15-stop electric tram, 900,000 AI chips cited by a US committee).
- Three illustrated heroes: the AI selloff deepening across Asian
  markets, Anthropic's record IPO debut, and Saudi Arabia's
  interception of a Houthi missile.
- Eight numbered stories in a photo grid: Indonesia's
  asset-forfeiture bill, Marcos urging AI adoption at APEC,
  Singapore's agent-led bill payments, Chiang Mai's e-tram, Hai
  Phong courting Chinese investment, a 1,275 MW wind study in Laos,
  Haiti's gang-raid toll, and the trilateral summit's narrow
  agreement on Ukraine.
- A "Where it happened" world map with numbered pins, and an
  eight-item Global Brief of the day's remaining wires.

## Files

- `entry.png` — the entry image (palette PNG, 819x1024).
- `main.py` — the submitted entrypoint: Python 3 standard library
  only, no network. It verifies `entry.png` against the bounty's
  limits (a whole PNG, at most 1 MiB, at most 1024x1024), copies it
  byte-for-byte to `/output/entry.png` (or a directory named by an
  optional positional argument), and confirms the copy by SHA-256.
  The same bytes come out on every run.
- `LICENSE` — MIT.

## Run

```sh
python3 main.py
```
