# Shinobu Music Bot — Config Vars

Config vars are the environment variables that configure the bot. They work the same way regardless of where you deploy — just set them in the right place for your platform.

---

## How Env Vars Work Across Platforms

| Platform | Where to set vars |
|----------|-------------------|
| **VPS / Docker** | Fill in `sample.env`, rename to `.env` |
| **Render** | Dashboard → Your Service → **Environment** tab |
| **Railway** | Dashboard → Your Project → **Variables** tab |
| **Replit** | Left sidebar → **Secrets** (🔒 icon) |

All platforms inject vars into `os.environ` — the bot reads them the same way everywhere.

---

## Mandatory Vars

These are required. The bot won't start without them.

| Var | Description |
|-----|-------------|
| `API_ID` | Get from [my.telegram.org](https://my.telegram.org) |
| `API_HASH` | Get from [my.telegram.org](https://my.telegram.org) |
| `BOT_TOKEN` | Get from [@BotFather](https://t.me/BotFather) |
| `MONGO_DB_URI` | MongoDB connection string — [get one free at MongoDB Atlas](https://www.mongodb.com/atlas) |
| `LOG_GROUP_ID` | A private supergroup ID (starts with -100) for bot logs |
| `MUSIC_BOT_NAME` | Your bot's display name (ASCII only, keep it simple) |
| `OWNER_ID` | Your Telegram user ID (integer) |
| `STRING_SESSION` | Pyrogram string session for the assistant account |

---

## Spotify Vars

Required only if you want Spotify link support. Spotify tracks resolve to YouTube for streaming.

| Var | Description |
|-----|-------------|
| `SPOTIFY_CLIENT_ID` | Get from [developer.spotify.com/dashboard](https://developer.spotify.com/dashboard) |
| `SPOTIFY_CLIENT_SECRET` | Get from [developer.spotify.com/dashboard](https://developer.spotify.com/dashboard) |

---

## Lyrics Vars

Required only if you want `/lyrics` command support.

| Var | Description |
|-----|-------------|
| `GENIUS_API_KEY` | Get from [genius.com/api-clients](https://genius.com/api-clients) |

---

## Optional Vars

Leave blank to use defaults.

### Audio & Limits

| Var | Default | Description |
|-----|---------|-------------|
| `DURATION_LIMIT` | `80` | Max stream duration in voice chat (minutes) |
| `SONG_DOWNLOAD_DURATION_LIMIT` | `180` | Max duration for song downloads (minutes) |
| `TG_AUDIO_FILESIZE_LIMIT` | `104857600` | Max Telegram audio file size in bytes (default 100MB) |
| `PLAYLIST_FETCH_LIMIT` | `20` | Max songs fetched from a playlist (hard capped at 20) |
| `SERVER_PLAYLIST_LIMIT` | `30` | Max playlists a user can save on the server |

### Assistant Behaviour

| Var | Default | Description |
|-----|---------|-------------|
| `AUTO_LEAVING_ASSISTANT` | `None` | Set `True` to auto-leave assistant from inactive chats |
| `ASSISTANT_LEAVE_TIME` | `5400` | Seconds before assistant auto-leaves (default 90 mins) |
| `AUTO_DOWNLOADS_CLEAR` | `None` | Set `True` to delete downloads after playback ends |
| `CLEANMODE_MINS` | `5` | Minutes before bot deletes its old messages from chat |

### Downloader

| Var | Default | Description |
|-----|---------|-------------|
| `YOUTUBE_EDIT_SLEEP` | `3` | Seconds between progress edits during YouTube download |

### Bot Setup

| Var | Default | Description |
|-----|---------|-------------|
| `SET_CMDS` | `False` | Set `True` to auto-register bot commands in chat menu |

---

## Multi-Assistant Mode

Run up to 5 assistant accounts simultaneously (supports ~2000–2500 chats at once).

| Var | Description |
|-----|-------------|
| `STRING_SESSION2` | Second assistant session |
| `STRING_SESSION3` | Third assistant session |
| `STRING_SESSION4` | Fourth assistant session |
| `STRING_SESSION5` | Fifth assistant session |

---

## Thumbnails

All thumbnails use a single fixed base image at `assets/thumbnail.jpeg` with text overlaid dynamically (song title, duration, requested by). No image URL vars are needed or supported.

| Asset | Used When |
|-------|-----------|
| `assets/thumbnail.jpeg` | All song playback, queue, skip |
| `assets/Ping.jpeg` | `/ping` command |
| `assets/Stats.jpeg` | `/stats` command |
| `assets/Global.jpeg` | Global stats |
| `assets/font.ttf` | Primary thumbnail font |
| `assets/font2.ttf` | Secondary thumbnail font |