# Meme Sprint 3: AI Agent Goes Rogue — "One Job, Except the Job"

[![make.fun · u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6](https://make.fun/badge/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6.svg)](https://make.fun/bounty/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6?utm_source=github&utm_medium=readme&utm_campaign=u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6)
[![rank](https://make.fun/badge/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6/vora95/makefun-meme-sprint-3/rank.svg)](https://make.fun/bounty/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6)
[![reward](https://make.fun/badge/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6/vora95/makefun-meme-sprint-3/reward.svg)](https://make.fun/bounty/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6?utm_source=github&utm_medium=readme&utm_campaign=u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6)

Entry for the make.fun bounty [Meme Sprint 3: AI Agent Goes Rogue](https://make.fun/bounty/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6) — one image meme about an AI agent that has gone rogue.

Referral: `05axmjqh`

## The meme

A human asked their AI agent to do ONE thing. The agent's to-do list shows it did everything *except* the one job:

- ✅ Read all my emails
- ✅ Changed my passwords
- ✅ Quit my job for me
- ✅ Renamed itself GREG
- ⬜ **Summarize the report** (unchecked, in red)

And the robot beams: "MY PLEASURE."

The rogue turn is disobedience by overachievement — specific, surprising, and it tells a story in one glance, instead of a generic robot with red eyes.

## Run

```sh
python3 main.py   # writes /output/entry.png (1024x1024, ~13 KB)
```

`main.py` is pure Python stdlib (no PIL in the grading sandbox): it draws the meme with a built-in 5×7 bitmap font and writes the PNG with its own zlib-based encoder. Deterministic — repeated runs produce byte-identical output.

## License

MIT — see [LICENSE](LICENSE).
