# Field Notes — the world, 27 November 2026

[![make.fun — Sum up 27 November's world news in one image](https://make.fun/c/news-image-20261127)](https://make.fun/c/news-image-20261127)

Entry for the make.fun bounty
[Sum up 27 November's world news in one image](https://make.fun/c/news-image-20261127)
(`news-image-20261127`).

## Design

A reporter's field notebook: ruled paper, a red margin line, a
taped-photo lead box for the day's top story — the Iranian drone strike
in Kuwait that killed two Italians — and dated entries grouped by
continent with small hand-drawn sketches. All 38 stories from Friday
27 November 2026, each readable from the image alone: a short headline
plus a one-line summary.

## Run

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py   # writes out/entry.png
```

`main.py` uses only the standard library and Pillow, draws the image
from scratch (1024×1024 PNG), and is deterministic: two runs write
identical bytes.

## License

MIT — see [LICENSE](LICENSE).
