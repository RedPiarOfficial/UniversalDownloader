from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
from rich.text import Text
from rich.align import Align
import yt_dlp
import phub
from phub import Quality
import phub.modules.download as download
from options import yt_opt, yt_opt_meta, tiktok_opt, tiktok_opt_meta
import uuid
import os
import re
class AppTikTok:
	def __init__(self, object, console):
		self.console = console
		self.TikTok = object

	def display_dataVideoInfo(self, data):
		os.system('cls')
		menu = {
			'1': 'download'
		}
		table = Table(title="VideoData")
		table.add_column("ID", justify="center", style="cyan", no_wrap=True)
		table.add_column("title", style="magenta")
		table.add_column("duration", justify="right", style="green")
		table.add_column("views", justify="right", style="green")
		table.add_column("likes", justify="right", style="green")
		table.add_column("upload_date", justify="right", style="green")
		table.add_column("uploader", justify="right", style="green")

		table.add_row(data['id'], data['title'], data['duration'], data['view_count'], data['like_count'], data['upload_date'], data['uploader'])
		self.console.print(table)
		for key, value in menu.items():
			self.console.print(f"[bold cyan]{key}[/bold cyan]: {value}")
		choice = Prompt.ask("Выберите опцию", choices=list(menu.keys()), default="1")
		if choice == '1':
			os.system('cls')
			self.console.print('[System]Загрузка начата')
			self.TikTok.download_video()

class AppPornHub:
	def __init__(self, console):
		self.console = console

	def display_dataVideoInfo(self, data):
		os.system('cls')
		menu = {
			'1': 'Download',
			'2': "Download Preview Photo",
			'3': 'Exit'
		}
		table = Table(title="VideoData")
		table.add_column("title", justify="center", style="cyan", no_wrap=True)
		table.add_column("author", style="magenta")
		table.add_column("views", justify="right", style="green")
		table.add_column("likes", justify="right", style="green")
		table.add_column("dislikes", justify="right", style="green")
		table.add_column("duration", justify="right", style="green")

		table.add_row(data['title'] if len(data['title']) < 15 else data['title'][:15] + '...', data['author'], data['views'], data['likes'], data['dislikes'], data['duration'])
		self.console.print(table)
		for key, value in menu.items():
			self.console.print(f"[bold cyan]{key}[/bold cyan]: {value}")
		choice = Prompt.ask("Выберите опцию", choices=list(menu.keys()), default="3")
		if choice == '1':
			new_name = f'{uuid.uuid4()}.mp4'
			threads = self.console.input(f'[System] Отправьте количество потоков: ')

			os.system('cls')
			self.console.print('[System] Загрузка начата')
			data['videoOBJ'].download(path = f'./videos/PornHub/{new_name}', quality = Quality.BEST, downloader = download.threaded(max_workers = 1 if type(threads) is not int else threads, timeout = 30))
			os.system('cls')
			self.console.print(f'[Download] видео сохранено: ./videos/PornHub/{new_name}')
			self.console.input('[Action] Press: ')
		elif choice == '2':
			new_name = f'{uuid.uuid4()}.jpg'
			self.console.print('[System] Загрузка начата')
			data['image'].download(f'./videos/PornHub/images/{new_name}')
			self.console.print(f'[Download] Изображение сохранено: ./videos/PornHub/images/{new_name}')
			self.console.input('[Action] Press: ')

class AppYouTube:
	def __init__(self, object, console):
		self.console = console
		self.YouTube = object

	def display_dataAllVideoInfo(self, data):
		os.system('cls')
		videosListDataRAM = []
		menu = {
			'1': 'Download',
			'2': 'Exit'
		}
		table = Table(title="VideoData")
		table.add_column("Download ID", justify="center", style="cyan", no_wrap=True)
		table.add_column("id", justify="center", style="cyan")
		table.add_column("url", style="magenta")
		table.add_column("title", justify="right", style="green")
		table.add_column("duration", justify="right", style="green")
		table.add_column("views", justify="right", style="green")

		for idx, video in enumerate(data):
			videosListDataRAM.append(video['url'])
			table.add_row(str(idx), video['id'], video['url'], video['title'] if len(video['title']) < 15 else video['title'][:15] + '...', video['duration'], video['views'])
		self.console.print(table)
		for key, value in menu.items():
			self.console.print(f"[bold cyan]{key}[/bold cyan]: {value}")
		choice = Prompt.ask("Выберите опцию", choices=list(menu.keys()), default="2")
		if choice == '1':
			DownloadID = self.console.input('[Action] Отправьте Download ID: ')
			self.console.print('[System] Загрузка начата')
			yt_opt['outtmpl'] = f"./videos/YouTube/Channels/%(uploader)s/%(title)s.%(ext)s"
			with yt_dlp.YoutubeDL(yt_opt) as ydl:
				ydl.download([videosListDataRAM[int(DownloadID)]])
			os.system('cls')
			self.console.print(f'[Download] видео сохранено в: ./videos/YouTube')
			self.console.input('[Action] Press: ')

	def display_dataVideoInfo(self, data):
		os.system('cls')
		menu = {
			'1': 'Download',
			'2': 'Exit'
		}
		table = Table(title="VideoData")
		table.add_column("id", justify="center", style="cyan", no_wrap=True)
		table.add_column("title", style="magenta")
		table.add_column("duration", justify="right", style="green")
		table.add_column("views", justify="right", style="green")
		table.add_column("likes", justify="right", style="green")
		table.add_column("upload_date", justify="right", style="green")
		table.add_column("uploader", justify="right", style="green")
		table.add_row(data['id'], data['title'] if len(data['title']) < 20 else data['title'][:20] + '...', data['duration'], data['view_count'], data['like_count'], data['upload_date'], data['uploader'])
		self.console.print(table)
		for key, value in menu.items():
			self.console.print(f"[bold cyan]{key}[/bold cyan]: {value}")
		choice = Prompt.ask("Выберите опцию", choices=list(menu.keys()), default="2")
		if choice == '1':
			self.console.print('[System] Загрузка начата')
			self.YouTube.download_video()

class AppAnimeJutSuSite:
	def __init__(self, object, console):
		self.console = console
		self.JutSu = object

	def display_dataAnimeInfo(self):
		os.system('cls')
		menu = {
			'1': 'Download Episode',
			'2': 'Download Season',
			'3': 'Download Anime',
			'4': 'Exit'
		}
		DownloadIDSet = 0
		DownloadIDSeasonSet = 0
		data = self.JutSu.get_anime_info()
		table = Table(title="AnimeData")
		table.add_column("DownloadID | SeasonID", justify="center", style="cyan", no_wrap=True)
		table.add_column("Anime", style="magenta")
		table.add_column("Season", justify="right", style="green")
		table.add_column("Episode", justify="right", style="green")
		table.add_column('URL', justify="right", style="green")

		for dicted in data.items():
			season = dicted[0]
			episodes = dicted[1]
			for episode in episodes:
				table.add_row(f'{DownloadIDSet}|{DownloadIDSeasonSet}', re.search(r'https?://[^\s/]+/([a-zA-Z0-9-]+)/?', self.JutSu.url).group(1), season if len(season) < 20 else season[:20] + '...', re.search(r'/episode-(\d+)\.html' if 'episode' in episode else r'/film-(\d+)\.html', episode).group(1), episode)
				DownloadIDSet += 1
			DownloadIDSeasonSet += 1
		self.console.print(table)
		for key, value in menu.items():
			self.console.print(f"[bold cyan]{key}[/bold cyan]: {value}")
		choice = Prompt.ask("Выберите опцию", choices=list(menu.keys()), default="4")
		if choice == '1':
			DownloadID = self.console.input('[Action] Отправьте Download ID: ')
			link = self.JutSu.get_anime_download_best_link(int(DownloadID))
			os.system('cls')
			self.JutSu.download_anime_episode(link, int(DownloadID))
		elif choice == '2':
			DownloadID = self.console.input('[Action] Отправьте Season ID: ')
			os.system('cls')
			self.JutSu.download_anime_season(int(DownloadID))
		elif choice == '3':
			self.JutSu.download_anime()

#https://www.youtube.com/@marazmatik re.search(r'https?://[^\s/]+/([a-zA-Z0-9-]+)/?', self.JutSu.url).group(1)
