[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/sholaah/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard)
[![reward](https://make.fun/badge/news-image-20261120/sholaah/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120)

# The World Today — 20 November 2026 in one image

A Python program that draws a single front page summing up the world
news of Friday 20 November 2026, in the style of a newspaper cover:
a red masthead, the date as the title, and the day's stories as drawn
panels with short headlines.

The day's selection:

- **The Hague** — UN judges rule that Myanmar's army committed genocide
  against the Rohingya, the court's first verdict of its kind.
- **Shenzhen** — Trump, Xi and Putin meet and issue a joint
  "peace declaration".
- **New York** — Anthropic, the first pure AI company to list, makes a
  record stock-market debut.
- **Berlin / Antalya / Riyadh** — Europe readies Ukraine talks with
  Russia; COP31's draft drops fossil fuels to outcry; a Houthi missile
  hits Riyadh's tallest tower as a tanker burns at Hormuz.
- And farewell to Fiona, Cincinnati's beloved hippo.

## Run

`python3 build_image.py` renders the cover (pure PIL, fixed inputs —
no network, no randomness — so every render is byte-identical) and
the result is committed as `entry.png`. `python3 main.py`, the
entrypoint, copies that file to `/output` (or `$MAKEFUN_OUTPUT_DIR`
when set) using only the standard library.
