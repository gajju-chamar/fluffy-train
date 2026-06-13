# Shinobu Music Bot
# Owner: @Sanji_fr

HELP_1 = """✅ **<u>Admin Commands:</u>**

**c** stands for channel play.

/pause or /cpause — Pause the playing track.
/resume or /cresume — Resume the paused track.
/mute or /cmute — Mute the playing track.
/unmute or /cunmute — Unmute the muted track.
/skip or /cskip — Skip the current playing track.
/stop or /cstop — Stop playback entirely.
/shuffle or /cshuffle — Randomly shuffle the queued playlist.
/seek or /cseek — Seek forward to a specific duration.
/seekback or /cseekback — Seek backward to a specific duration.
/restart — Restart the bot for your chat.

✅ <u>**Specific Skip:**</u>
/skip [Number] — Skip to a specific position in the queue.
Example: /skip 3 skips directly to track 3, ignoring tracks 1 and 2.

✅ <u>**Loop Play:**</u>
/loop [enable/disable] or [1-10] — Loop the current track 1–10 times. Defaults to 10.

✅ <u>**Auth Users:**</u>
Auth users can use admin commands without having admin rights.

/auth [Username] — Add a user to the group's auth list.
/unauth [Username] — Remove a user from the group's auth list.
/authusers — View the group's auth list."""


HELP_2 = """✅ <u>**Play Commands:**</u>

/play or /cplay — Play a song or stream a live link in voice chat.
/playforce or /cplayforce — Force play: stops the current track and plays the new one instantly without clearing the queue.
/channelplay [username/id] or [disable] — Connect a channel to stream music on its voice chat from your group.

**c** stands for channel play.
**force** stands for force play.

✅ **<u>Server Playlists:</u>**
/playlist — View your saved server playlist.
/deleteplaylist — Delete a saved track from your playlist.
/play — Start playing your saved server playlist."""


HELP_3 = """✅ <u>**Bot Commands:**</u>

/stats — Get top 10 global tracks, top users, top chats, and more.
/sudolist — View sudo users of Shinobu.
/lyrics [Track Name] — Search for lyrics of a track.
/song [Track Name or YouTube link] — Download a track from YouTube in MP3 format.
/queue or /cqueue — View the current music queue.

**c** stands for channel play."""


HELP_4 = """✅ <u>**General Commands:**</u>
/start — Start the bot.
/help — Get the help menu.
/ping — Check bot latency and server stats.

✅ <u>**Group Settings:**</u>
/settings — Open the group settings panel.

🔗 **Settings Options:**

1️⃣ **Audio Quality** — Set the streaming audio quality.

2️⃣ **Auth Users** — Toggle admin commands between everyone or admins only.

3️⃣ **Clean Mode** — Auto-delete bot messages after 5 minutes to keep your chat tidy.

4️⃣ **Command Clean** — Auto-delete executed commands (/play, /pause, etc.) immediately.

5️⃣ **Play Settings** — Use /playmode for a full play settings panel.

<u>Playmode options:</u>

1️⃣ **Search Mode** [Direct or Inline] — Change how /play handles search queries.

2️⃣ **Admin Commands** [Everyone or Admins] — Control who can use admin commands.

3️⃣ **Play Type** [Everyone or Admins] — Control who can queue music."""


HELP_5 = """🔰 **<u>Sudo Users:</u>**
/addsudo [Username or reply] — Add a sudo user.
/delsudo [Username or reply] — Remove a sudo user.

🌐 **<u>Config Vars:</u>**
/vars — View current bot configuration.

🤖 **<u>Bot Commands:</u>**
/reboot — Reboot the bot.
/speedtest — Check server speeds.
/maintenance [enable/disable] — Toggle maintenance mode.
/logger [enable/disable] — Log searched queries to your log group.
/autoend [enable/disable] — Auto-end stream after 3 minutes if no one is listening.

📈 **<u>Stats Commands:</u>**
/activevoice — Check active voice chats.
/stats — Check bot stats.

⚠️ **<u>Blacklist:</u>**
/blacklistchat [CHAT_ID] — Blacklist a chat.
/whitelistchat [CHAT_ID] — Whitelist a blacklisted chat.
/blacklistedchat — View all blacklisted chats.

👤 **<u>Block Users:</u>**
/block [Username or reply] — Block a user from using the bot.
/unblock [Username or reply] — Unblock a user.
/blockedusers — View blocked users.

👤 **<u>Global Ban:</u>**
/gban [Username or reply] — Globally ban a user from all served chats.
/ungban [Username or reply] — Remove a global ban.
/gbannedusers — View globally banned users.

⚡️ **<u>Approve System:</u>**
/approve [CHAT_ID] — Allow a chat to use Shinobu.
/unapprove [CHAT_ID] — Revoke a chat's access.
/approvedchats — View all approved chats.

🌐 **<u>Broadcast:</u>**
/broadcast [Message or reply] — Broadcast to all served chats.

Options:
**-pin** — Pin the message.
**-pinloud** — Pin with loud notification.
**-user** — Broadcast to users who started the bot.
**-assistant** — Broadcast from the assistant account.
**-nobot** — Skip the bot's own broadcast.

Example: `/broadcast -user -pin Hello everyone~`"""