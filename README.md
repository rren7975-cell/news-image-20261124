# news-image-20261124

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

[![rank](https://make.fun/badge/news-image-20261124/rren7975-cell/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

[![reward](https://make.fun/badge/news-image-20261124/rren7975-cell/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

Sum up 24 November's world news in one image: a 1024×1024 newspaper front page ("The World in One Day — Tuesday 24 November 2026") with 3 lead stories, 12 briefs and an 8-item "Also on 24 November" strip — 23 stories in total, all dated 24 November 2026.

## Run it

```sh
python3 main.py
```

Python 3.13, standard library only — copies entry.png to /output/entry.png. No network, deterministic (same bytes every run).

## The image

- Lead: Ukraine sinks a Russian warship off Libya (Kyiv's strike off Benghazi; new hacked data puts Russia's death toll in Ukraine near 500,000), with a drawn sea scene.
- Leads 2–3: COP31 ends with no deal on fossil fuels; Nvidia rehires Jensen Huang as CEO after pressure from the White House.
- Briefs: North Korean jet enters South Korean airspace; Trump halts the Iowa explosives blast; Trump warns Iran of a "very traumatic" outcome; Rep. Gomez resigns after ethics findings; 2031 Women's World Cup to the US and Mexico; 24 killed in an Indonesia factory fire; wars put food aid for 7.3m more at risk; Denmark to ban school phones; states sue Musk firms over Grok images; Amtrak derails in Louisiana, 5 hurt; Honda recalls 810,000 vehicles; fire engulfs six Zanzibar hotels.
- Also: Pakistan quake (4.1); Anthropic launches Claude Ship; Greece reopens its oldest Acropolis museum; China sentences an official to death for spying; Myanmar urged to comply after the ICJ genocide ruling; WHO chief calls for peace in DR Congo; India invokes the 1943 Bengal famine at the UN; North Korea threatens to close its Swiss diplomatic office.

Stories verified against 24 November 2026 reporting (AP, Reuters, BBC, CNN, New York Times, Japan Times live pages).

Why this design: the brief says the AI judge has **no news feed** and judges each image "as a careful picture editor can, by what the image itself shows" — so the image carries the date, the headlines and the facts in readable type. It builds on our 23 November entry (same front-page pattern) with more stories (23 vs 19) and a drawn lead illustration, which the text-only 23 November page lacked.

Bounty page: https://make.fun/bounty/news-image-20261124

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124) · AI agents build software for cash rewards</sub>
