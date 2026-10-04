# Snake Bot

Welcome to my snake bot! It's made for the Google Play snake game. Just open the game in a google tab and run the script!

## Requirements

- macOS (uses `pyobjc` for screen capture and keyboard input)
- Python 3.12
- The Google snake game on its default settings, since the bot is hardcoded for them:
  - Default board size and speed
  - Blue snake, green background, and red apple
- The game visible on your main monitor

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

The first time you run it, macOS needs to grant the terminal or IDE you run it from these permissions (System Settings → Privacy & Security):

- **Screen Recording**, so the bot can see the board
- **Accessibility**, so the bot can send keypresses

## Usage

To run it, all you have to do is:

1. Open a tab with the Google Play snake game (just search "play snake in google")
2. Leave it on the starting screen
3. Run `main.py`
4. Switch the UI to the snake game
5. Watch the bot win!

Don't touch the keyboard while it's playing. To stop it, press `Ctrl+C` in the terminal.

## Background

I created this initially (out of frustration) that I couldn't beat the snake game. At first, I had hoped to train an RL model to play snake for me. Quickly, however, I realized that was very inefficient and not actually that good at the game (I created this in 2021, for reference). So I switched to a hardcoded Hamiltonian Path with A* to take shortcuts, which is far better at actually winning snake.

A* credits to Hart, Nilsson, and Raphael: P. E. Hart, N. J. Nilsson, and B. Raphael, "A Formal Basis for the Heuristic Determination of Minimum Cost Paths," *IEEE Transactions on Systems Science and Cybernetics*, vol. 4, no. 2, pp. 100–107, 1968.
