# demo

recorded solver games and a script that turns them into a video.

```
python3 record.py --depth 3 --seed 29 --out demo/game.json
python3 demo/render.py demo/game.json demo/demo.mp4 --seconds 45
```

`render.py` needs pillow and ffmpeg.

- `game.json`, `demo.mp4`: depth 3, seed 29, score 61020, reaches 4096
- `game_d2.json`, `demo_depth2.mp4`: depth 2, seed 3, score 52920, reaches 4096

both are among the best games of their agent, not typical ones.
typical numbers are in `results/README.md`.
