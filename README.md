# Beatle Discord Bot Framework

Beatle is a small framework for building Discord bots using [discord.py](https://discordpy.readthedocs.io/).

## Features

- Minimal wrapper around `commands.Bot` with automatic cog loading
- Example `ping` cog
- Basic Spotify search command
- Ready for extension with your own modules

## Quick start

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Create a bot script:

```python
from beatle import BeatleBot

bot = BeatleBot()

bot.run("YOUR_TOKEN_HERE")
```

3. Add additional cogs under `beatle/cogs` or specify your own package.

Set `SPOTIFY_CLIENT_ID` and `SPOTIFY_CLIENT_SECRET` environment variables to enable Spotify commands.

## Testing

Run the unit tests with:

```bash
python -m pytest -q
```
