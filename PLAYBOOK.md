# Daily Pin Playbook – Fit Essentials (Pinterest: Lildesports)

The daily scheduled session follows this file. Goal: publish **2 new pins per day** that follow the
pattern of the account's best performers, without the owner having to do anything.

## Daily run

1. Work in this repository (`leonhaupt08-ui/fit-pins`, branch `main`).
2. Open `queue.json`. Take the **2 oldest entries with `"status": "queued"`** whose image
   `pins/<slug>.jpg` exists in the repo **and was pushed in an earlier run** (GitHub Pages needs a
   minute or two to publish new files – never post an image pushed in the same run).
3. Post each one with the Zapier tool `pinterest_create_pin` (selected_api `PinterestCLIAPI`,
   action `create_pin`):
   - `board_id`: entry `board_id`
   - `image_url`: `https://leonhaupt08-ui.github.io/fit-pins/pins/<slug>.jpg`
   - `source_url`: entry `product_url`
   - `title`, `description`: from the entry
4. On success set `"status": "posted"`, `"posted_at": "<YYYY-MM-DD>"`, `"pin_id": "<id>"`.
   On failure set `"status": "failed"` and `"error": "<short reason>"` and do not retry more than once.
5. If fewer than **6** entries are `queued`, create **6 new entries** (see below), render them with
   `node tools/render.js`, look at every rendered image (crop, readability) and fix bad ones.
6. Commit and push (`git -c push.negotiate=true push origin main`). Commit message: `Daily pins <date>`.
7. Finish with a short summary in German: which pins were posted (with links
   `https://www.pinterest.com/pin/<pin_id>/`), how many are still queued.

**Stop conditions:** if Zapier says the Pinterest connection needs a paid plan, is stale or needs
reconnecting, do **not** keep trying. Post nothing, send a push notification in German saying that the
Zapier trial/connection has ended and the owner should tell Claude, and end the run.

## Creating new entries

Source products from the account's own existing pins (they already carry the affiliate tag `lilmedia-21`):

1. Read the account's pins via Zapier `pinterest_make_api_get_request`
   (`https://api.pinterest.com/v5/pins`, `page_size` 100, follow `bookmark`). Large results are saved to
   a file – parse that file with Python instead of reading it into context.
2. Optionally read `https://api.pinterest.com/v5/user_account/analytics/top_pins`
   (`sort_by` IMPRESSION or SAVE, last 90 days) to prefer what performs.
3. Only use pins whose link is `amazon.de` and whose ASIN (the 10 characters after `/dp/`) is **not**
   already in `queue.json`. Skip pins whose image is not portrait (height < width).
4. Priority: **outfits / clothing** (leggings, sweatpants, gym sets, shorts, tops, hoodies) first –
   these bring ~90 % of the account's reach. Equipment and gadgets only occasionally (max 1 of 6).
5. Each entry:
   - `slug`: next running number + short kebab-case name, e.g. `12-black-seamless-leggings`
   - `product_url`: `https://www.amazon.de/dp/<ASIN>?tag=lilmedia-21`
   - `source_image`: the pin's `media.images["1200x"].url`
   - `board_id`: see table below
   - `tag`: `OUTFIT IDEA` for clothing, `GYM ESSENTIALS` for equipment, `RECOVERY` for recovery
   - `headline`: 2–3 short lines in CAPS, separated by `<br>`, max ~12 characters per line,
     search-style words (e.g. `BLACK<br>LEGGINGS<br>GYM OUTFIT`). Never repeat a headline already used.
   - `subline`: one short English line (e.g. `High waist · seamless · easy to style`)
   - `position`: CSS background-position that keeps the product visible (default `center 35%`)
   - `title`: English, keyword first, max 100 characters, no hype (e.g.
     `Black Leggings Gym Outfit | High Waist Seamless Leggings`)
   - `description`: 2 English sentences with search keywords and styling idea, then a blank line,
     `Werbung | Affiliate-Link`, blank line, 4–5 hashtags
   - `status`: `queued`

## Rules (must follow)

- Every description contains `Werbung | Affiliate-Link` (German law).
- No health or weight-loss promises ("lose weight", "burn fat", "cures", "boosts testosterone" …).
- No other brands' logos in the overlay text; product photos stay as they are.
- Max 2 pins per day, never the same product twice within 14 days.
- Never edit or delete existing pins, boards or the profile.

## Boards

| Board | id |
|---|---|
| Men's Gym Outfits & Athleisure | 1110207814332820701 |
| Gym Leggings Outfits for Women | 1110207814332818580 |
| Women's Gym Outfits \| Workout Fits | 1110207814332818565 |
| Women's Gym Shorts \| Workout Shorts | 1110207814332820674 |
| Women's Gym Tops & Sports Bras | 1110207814332850044 |
| Men's Gym & Running Shoes | 1110207814332971379 |
| Women's Gym & Running Shoes | 1110207814332963572 |
| Gym Equipment & Workout Essentials | 1110207814332816389 |
| Muscle Recovery & Sleep Essentials | 1110207814332963633 |
