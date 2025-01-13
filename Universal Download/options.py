yt_opt = {
	'format': 'best',
	'outtmpl': '%(title)s.%(ext)s',
}

yt_opt_meta = {
	'extract_flat': True,
    'quiet': True
}
tiktok_opt = {
	'outtmpl': '%(title)s.%(ext)s',
    'format': 'bestvideo+bestaudio/best',
    'merge_output_format': 'mp4', 
    'noplaylist': True,
}

tiktok_opt_meta = {
	'extract_flat': True,
    'quiet': True
}

headers = {
  "accept": "*/*",
  "accept-encoding": "gzip, deflate, br, zstd",
  "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
  "cache-control": "no-cache",
  "origin": "https://jut.su",
  "pragma": "no-cache",
  "priority": "u=1, i",
  "referer": "https://jut.su/",
  "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
  "sec-ch-ua-mobile": "?0",
  "sec-ch-ua-platform": "\"Windows\"",
  "sec-fetch-dest": "empty",
  "sec-fetch-mode": "cors",
  "sec-fetch-site": "cross-site",
  "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}