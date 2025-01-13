# UniversalDownloader
UniversalDownloader is a versatile tool for downloading videos from various platforms, including YouTube, TikTok, AnimeJutSuSite, and PornHub.

**Version**: Beta0.1.0

**Supported Languages**: ru

## BetaTest Goal
Collect feedback from users, identify bugs, and improve the product before the final release.
## Key Features
- Support for downloading videos, playlists, and channels from YouTube.
- Download anime (episodes, seasons, all seasons).
- Download TikTok videos without watermarks.
- Download videos and previews from PornHub.
- Fast download speed, adaptable to internet quality.

## Futures
### Anime
1. **Download Episode**
   - Downloads a single anime episode.
   - Requires: DownloadID from the table (starting from zero).
2. **Download Season**
   - Downloads all episodes from the specified season.
   - Requires: SeasonID from the table (starting from zero).
3. **Download Anime**
   - Downloads all seasons and movies of the anime.

### YouTube
1. **Download Video**
   - Downloads a single video.
   - Example: https://www.youtube.com/watch?v=pk8H_yNm8jY&t=3s
2. **Download Playlist**
   - Downloads all videos from the specified playlist.
   - Example: https://www.youtube.com/watch?v=f18jsyBpo7M&list=PLweuMCWXrp0Lg7Hrz2bQYkinusn27siLF
3. **Download Videos from Channel**
   - Downloads all videos from the specified channel.
   - Example: https://www.youtube.com/@windy31LetsGoodPlays

### TikTok
1. **Download Video**
   - Downloads video without a watermark.

### PornHub
1. **Download Video**
   - Downloads the video in the best quality.
2. **Download Preview**
   - Downloads the preview of the specified video.

## Download Speed
Testing was conducted with an internet speed of 180 Mbps. Results:

1. **Anime**: Download in ~50 seconds (one episode).
2. **YouTube**: Download in ~30 seconds.
3. **TikTok**: Almost instant download.
4. **PornHub**: Download time ranges from 10 seconds.

**Note**: Download time depends on the video's resolution, length, and the quality of your internet connection.

## Advantages
- **Efficiency**: Asynchronous downloads speed up the process.
- **Cross-platform**: Support for videos from various sites.
- **Simplicity**: Convenient CLI interface.

## Future Plans
1. **Adding New Platforms**:
   - Support for other popular video services.
2. **Quality Selection**:
   - Ability to choose video resolution before downloading.
3. **Performance Improvement**:
   - Optimization for slow internet connections.
4. **Localization**:
   - Interface translation to other languages.

## Installation and Launch
1. Clone the repository:
```bash
git clone https://github.com/RedPiarOfficial/UniversalDownloader.git
```
2. Navigate to the project directory:
```bash
cd UniversalDownloader
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```
Run the script:
```bash
python client.py
```
Alternatively, you can download the repository archive: [UniversalDownloader.zip](https://github.com/RedPiarOfficial/UniversalDownloader/archive/refs/heads/main.zip)

## Technical Requirements
- Python 3.12+
- Installed modules from the requirements.txt file
## Contacts
Developer: RedPiar

Email: redxpiar@gmail.com

Telegram: @RedPiar

Channel: https://t.me/BotesForTelegram
