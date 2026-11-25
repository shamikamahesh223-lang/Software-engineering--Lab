# Scenario 21 — Checkers

A modular terminal checkers game with complete capture, king, promotion, forced-capture, multi-capture, win/no-move, and move-feedback support.

## Run

```bash
python3 main.py
```

Move format: `sr sc er ec` (row/column coordinates 0-7). Enter `q` to quit.

## Completed Tasks
- Task 1: Captures remove the jumped opponent and preserve the moving piece.
- Task 2: Game ends when a side has no pieces or no legal moves.
- Task 3: Forced captures, multi-capture turns, king movement in both directions, and promotion.
- Task 4: Concise move/capture/promotion feedback.

## Testing
Test ordinary moves, captures, multiple captures, forced captures, promotion, king movement, no-move positions, invalid coordinates, and quitting.
