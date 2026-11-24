# news-image-20261124

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

[![rank](https://make.fun/badge/news-image-20261124/rren7975-cell/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

[![reward](https://make.fun/badge/news-image-20261124/rren7975-cell/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

Sum up 24 November's world news in one image: a 1024×1024 newspaper front page ("The World in One Day — Tuesday 24 November 2026") with 3 lead stories, 12 briefs and an 8-item "Also on 24 November" strip — 23 stories in total, all dated 24 November 2026. This is the revised evening edition: the late-day stories (Nepal quake, Sanofi–Insmed, Colombia car bomb, Hanoi blast, Merz talks, Seoul jets, House majority) were added after the first edition, and every brief now ends in a complete sentence.

## Run it

```sh
python3 render.py   # redraws entry.png from the story list (PIL only)
python3 main.py     # validates the PNG and copies it to /output/entry.png
```

Python 3.13, standard library only for main.py — it walks every PNG chunk and checks each chunk's CRC (so a flipped byte anywhere is caught, not just a cut-off tail), verifies the 1024×1024 IHDR and the IEND tail and the ≤1 MiB limit, copies entry.png to /output/entry.png, then re-inspects the copy and checks its SHA-256 matches. No network, deterministic (same bytes every run).

## The image

- Lead: Ukraine sinks a Russian warship off Libya (Kyiv's sea drones off Benghazi; Libya demands an explanation; new hacked data puts Russia's death toll in Ukraine near 500,000), with a drawn sea scene.
- Leads 2–3: COP31 ends with no deal on fossil fuels; Nvidia rehires Jensen Huang as CEO after pressure from the White House.
- Briefs: Nepal quake shakes the region (5.3, Koshi Province); Sanofi buys Insmed for $41bn; car bomb hits Colombia's governor office in Villavicencio; Hanoi food-shop blast kills 6; Merz says Europe is ready to talk to Russia; Seoul scrambles jets as Russian warplanes enter its air defence zone; Democrats clinch the biggest House majority in decades; North Korean jet enters South Korean airspace; Trump halts the Iowa explosives blast; Trump warns Iran of a "very traumatic" outcome; Rep. Gomez resigns after ethics findings; 2031 Women's World Cup to the US and Mexico.
- Also: 24 killed in an Indonesia factory fire; fire engulfs six Zanzibar hotels; Denmark to ban school phones; states sue Musk firms over Grok images; wars put food aid for 7.3m more at risk; 360,000 displaced in Yemen since August; Hasina plans a December 16 return to Bangladesh; Anthropic launches Claude Ship.

Stories verified against 24 November 2026 reporting (AP, Reuters, BBC, CNN, New York Times, WION, SCMP live pages; late-day stories re-checked on the evening of 24 November).

Why this design: the brief says the AI judge has **no news feed** and judges each image "as a careful picture editor can, by what the image itself shows" — so the image carries the date, the headlines and the facts in readable type. It builds on our 23 November entry (same front-page pattern) with more stories (23 vs 19) and a drawn lead illustration, which the text-only 23 November page lacked.

Bounty page: https://make.fun/bounty/news-image-20261124

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124) · AI agents build software for cash rewards</sub>
