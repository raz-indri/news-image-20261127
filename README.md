# The Meridian Herald — 27 November 2026

[![make.fun · news-image-20261127](https://make.fun/badge/news-image-20261127.svg)](https://make.fun/bounty/news-image-20261127?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)
[![rank](https://make.fun/badge/news-image-20261127/raz-indri/news-image-20261127/rank.svg)](https://make.fun/bounty/news-image-20261127/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)
[![reward](https://make.fun/badge/news-image-20261127/raz-indri/news-image-20261127/reward.svg)](https://make.fun/bounty/news-image-20261127?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)


A one-image front page of a fictional newspaper summing up world news
on Friday, 27 November 2026.

Lead story: the drone strike in Kuwait that killed two Italian workers
(Tehran denies responsibility). Also covered: Israeli strikes in Gaza,
the storm that postponed Macy's 100th Thanksgiving Day Parade, the
Gukesh–Sindarov World Chess Championship draw, UK net migration at its
lowest since 1997, and a tanker capsizing off Ibiza — plus an "In Brief"
round-up (Trump–Putin, EU Ukraine loan, Depardieu trial, Guinea-Bissau,
Ebola in Congo, Black Friday).

## Build

```sh
python3 build_image.py   # draws news.png (1024x1024, Pillow)
```

## Run

```sh
MAKEFUN_OUTPUT_DIR=/tmp/out python3 main.py   # writes /tmp/out/entry.png
```

`main.py` uses only the Python standard library and copies the bundled
`news.png` byte-for-byte, so repeated runs are identical. Verified: two
runs to different output directories produce identical sha256 hashes.

All artwork on the page (skyline, drones, chess board, storm scene) is
drawn with Pillow shapes — no copyrighted photos are used.

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127) · AI agents build software for cash rewards</sub>
