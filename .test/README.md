# Headless test harness

`node smoke.mjs` boots `../index.html` in jsdom and drives the real UI across all five modes
(56 assertions). It needs `jsdom`, which is deliberately **not** committed:

```bash
npm i --no-save jsdom          # from .test/ (or repo root)
node smoke.mjs                 # or: DBG=1 node smoke.mjs to dump the view DOM per step
```

`node_modules/` and `package-lock.json` are git-ignored.
