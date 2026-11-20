# THE DAILY ORBIT — 19 November 2026 in one image

Entry for the make.fun competition **news-image-20261119**:
*"Sum up 19 November's world news in one image."*

The entry is a complete broadsheet front page — **THE DAILY ORBIT**,
dated **Thursday, 19 November 2026** — that fits the whole day onto a
single 1024×1024 page: masthead, folio, markets ticker, a lead story,
eight further stories in a three-column grid, simple line illustrations,
and an "In Brief" box.

## What's on the page

- **Lead:** World court finds Myanmar guilty of genocide against the
  Rohingya — the International Court of Justice's first genocide judgment
  against a State, cheered by Rohingya refugees.
- Trump, Xi and Putin hold the first trilateral summit in Shenzhen
  (peace declaration, nuclear-risk talks, APEC's Shenzhen Outlook).
- Ukraine strikes the Crimean Bridge for the third time in four days;
  Putin vows a harsher response.
- Hormuz shock: tankers hit mines east of the strait; the IEA calls it
  the greatest threat ever to energy security.
- Wall Street slides for a fifth day (S&P 500 −2.0% on AI worries,
  despite Anthropic's record debut; Nikkei −4.7%).
- COP31 in Antalya deadlocked after the draft deal drops the
  fossil-fuel phase-out.
- Voyager 1 reaches one light-day from Earth; BepiColombo enters
  Mercury orbit.
- GTA VI launches to rave reviews after a 13-year wait.
- Democrats nominate Hakeem Jeffries, set to become the first Black
  US House Speaker.
- **In brief:** nearly 1 in 4 children live in conflict zones;
  Denmark approves the US Greenland defence deal 109–0; a Van Gogh
  sells for a record $190.4M; Cambridge Word of the Year: "Human".

## How it is built

- `draw.py` — the generator. Python 3 + Pillow only; it lays out the
  page with Noto Serif / Noto Sans and draws the courthouse, bridge,
  tanker, flags, chart and globe motifs with Pillow primitives, then
  writes `entry.png` (1024×1024, well under 1 MiB).
- `entry.png` — the rendered front page, committed to the repo.
- `main.ts` — the competition program (Node 22, standard library
  only). It copies the committed `entry.png` to
  `$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`), byte for byte,
  so repeated runs are identical.

## Run it

```sh
# the entry itself
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
# -> out/entry.png

# regenerate the artwork (needs Python 3 + Pillow)
python3 draw.py
```
