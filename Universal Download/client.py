import os
import re
from tqdm import tqdm
import httpx
import yt_dlp
import phub
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from options import yt_opt, yt_opt_meta, tiktok_opt, tiktok_opt_meta, headers
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
from rich.text import Text
from rich.align import Align
from time import sleep
import uuid
from concurrent.futures import ThreadPoolExecutor
from Applications import AppTikTok, AppPornHub, AppYouTube, AppAnimeJutSuSite

console = Console()
os.makedirs('./videos/YouTube', exist_ok=True)
os.makedirs('./videos/YouTube/PlayList', exist_ok=True)
os.makedirs('./videos/YouTube/Channels', exist_ok=True)
os.makedirs('./videos/TikTok', exist_ok=True)
os.makedirs('./videos/Anime', exist_ok=True)
os.makedirs('./videos/PornHub', exist_ok=True)
os.makedirs('./videos/PornHub/images', exist_ok=True)

class JutSu:
	def __init__(self, url):
		self.url = url
		self.data = None
		self.DownloadIDsList = []

	def get_anime_info(self):
		"""Функция для получения все сезонов и эпизодов"""
		resp = requests.get(self.url, headers=headers)
		soup = BeautifulSoup(resp.text, "html.parser")

		class_pattern = re.compile(r"^b-b-title the-anime-season center")

		sections = soup.find_all("h2", class_=class_pattern)
		result = {}

		for i, section in enumerate(sections):
			title = section.get_text(strip=True)
			links = []

			# Найти все ссылки до следующей секции
			for tag in section.find_next_siblings():
				if tag.name == "h2":
					break
				if tag.name == "a" and "href" in tag.attrs:
					links.append(tag["href"])
					self.DownloadIDsList.append(tag['href'])
			
			result[title] = links

		if not result:
			links = []
			sections = soup.find_all("a", class_=re.compile(r"^short-btn"))
			for tag in sections:
				links.append(tag["href"])
				self.DownloadIDsList.append(tag['href'])
			result[re.search(r'https?://[^\s/]+/([a-zA-Z0-9-]+)/?', self.url).group(1)] = links

		self.data = result # Сохраняем для дальнейшего использования.

		return result

	def get_anime_download_best_link(self, DownloadID):
		response = requests.get('https://jut.su' + self.DownloadIDsList[DownloadID], headers=headers)
		soup = BeautifulSoup(response.text, "html.parser")
		video_element = soup.find("video", class_="video-js vjs-default-skin vjs-16-9")
		if video_element:
			sources = video_element.find_all("source")
			video_links = [source["src"] for source in sources if source.get("src")]
			if video_links:
				return video_links[0]
		return None

	def download_chunk(self, url, chunk_size, start_byte, end_byte, filename, progress):
		current_headers = headers.copy()
		with httpx.Client(http2=True) as client:
			current_headers['Range'] = f"bytes={start_byte}-{end_byte}"
			with client.stream("GET", url, headers=current_headers) as resp:
				resp.raise_for_status()
				# Вызов метода read() для получения данных из потока
				chunk_data = resp.read()
				with open(filename, "r+b") as f:
					f.seek(start_byte)
					f.write(chunk_data)
				progress.update(len(chunk_data))


	def download_anime_episode(self, DownloadLink, DownloadID=None, link=None):
		if link:
			season = re.search(r'/season-(\d+)', link)
			episode = re.search(r'/(episode|film)-\d+\.html', link)
		else:
			season = re.search(r'/season-(\d+)', self.DownloadIDsList[DownloadID])
			episode = re.search(r'/(episode|film)-\d+\.html', self.DownloadIDsList[DownloadID])

		season = season.group(1) if season else 'season-1'

		base_path = f'./videos/anime/{re.search(r"https?://[^\s/]+/([a-zA-Z0-9-]+)/", self.url).group(1)}'
		os.makedirs(base_path, exist_ok=True)
		if season:
			os.makedirs(f'{base_path}/{season}', exist_ok=True)

		console.print("[System] Загрузка начата.")

		with httpx.Client(http2=True) as client:
			resp = client.head(DownloadLink, headers=headers)
			resp.raise_for_status()
			total_size = int(resp.headers.get('content-length', 0))

		# Файл для сохранения
		filename = f'{base_path}/{season}/{episode.group(0)[1:-5]}.mp4' if season else f'{base_path}/{episode.group(0)[1:-5]}.mp4'
		
		with open(filename, "wb") as f:
			f.truncate(total_size)

		# Инициализируем прогресс бар
		with tqdm(total=total_size, unit='B', unit_scale=True, unit_divisor=1024, desc=f"Сезон {season}, Эпизод {episode.group(0)[1:-5]}") as progress:
			
			# Разделяем файл на чанки
			chunk_size = 1024 * 1024 * 10  # 10 MB
			num_chunks = total_size // chunk_size + (1 if total_size % chunk_size else 0)

			with ThreadPoolExecutor(max_workers=8) as executor:
				futures = []
				for i in range(num_chunks):
					start_byte = i * chunk_size
					end_byte = min((i + 1) * chunk_size - 1, total_size - 1)
					# передаем аргументы в download_chunk
					futures.append(executor.submit(self.download_chunk, DownloadLink, chunk_size, start_byte, end_byte, filename, progress))

				for future in futures:
					future.result()

		console.print(f'[Download] Видео сохранено: {filename}')

		if not link:
			console.input('[Action] Press: ')

	def download_anime_season(self, DownloadID):
		os.system('cls')
		for video in self.data[list(self.data.keys())[DownloadID]]:
			link = self._get_anime_download_best_link("https://jut.su" + video)
			self.download_anime_episode(link, link=video)
		console.input('[Action] Press: ')

	def download_anime(self):
		os.system('cls')
		for video in self.DownloadIDsList:
			link = self._get_anime_download_best_link("https://jut.su" + video)
			self.download_anime_episode(link, link=video)
		console.input('[Action] Press: ')

	def _get_anime_download_best_link(self, link):
		response = requests.get(link, headers=headers)
		soup = BeautifulSoup(response.text, "html.parser")
		video_element = soup.find("video", class_="video-js vjs-default-skin vjs-16-9")
		if video_element:
			sources = video_element.find_all("source")
			video_links = [source["src"] for source in sources if source.get("src")]
			if video_links:
				return video_links[0]
		return None

class YouTube:
	def __init__(self, url):
		self.url = url

	def get_videos_by_channel(self):
		videos = None
		format_videos = []
		with yt_dlp.YoutubeDL(yt_opt_meta) as ydl:
			info = ydl.extract_info(f"{self.url}/videos", download=False)
			if 'entries' in info:
				videos = info['entries']
		
		if videos:
			for video in videos:
				format_videos.append(
					{
					'id': str(video.get('id')),
					'url': video.get('url'),
					'title': video.get('title'),
					'duration': str(video.get('duration')),
					'views': str(video.get('view_count'))
				})

		return format_videos


	def get_video_info(self):
		with yt_dlp.YoutubeDL(yt_opt_meta) as ydl:
			info = ydl.extract_info(self.url, download=False)
			return {
				'title': info.get('title'),
				'id': str(info.get('id')),
				'duration': str(info.get('duration')),
				'view_count': str(info.get('view_count')),
				'like_count': str(info.get('like_count')),
				'upload_date': str(info.get('upload_date')),
				'uploader': info.get('uploader'),
			}

	def download_video(self, path='./videos/YouTube/Channels'):
		yt_opt['outtmpl'] = f"{path}/%(uploader)s/%(title)s.%(ext)s"
		with yt_dlp.YoutubeDL(yt_opt) as ydl:
			info = ydl.extract_info(self.url, download=False)
			ydl.download([self.url])
			os.system('cls')
			console.print(f'[Download] видео сохранено: ./videos/YouTube/{info.get("uploader")}/{info.get("title")}.{info.get("ext")}')
			console.input('[Action] Press: ')

	def download_all_video_by_channel(self, path='./videos/YouTube'):
		yt_opt['outtmpl'] = f"{path}/%(uploader)s/%(title)s.%(ext)s"
		try:
			with yt_dlp.YoutubeDL(yt_opt) as ydl:
				ydl.download([f"{self.url}/videos"])
				os.system('cls')
				console.print(f'[Download] все видео с канала сохранены')
				console.input('[Action] Press: ')
		except:
			pass

	def download_playlist(self, path='./videos/YouTube/PlayList'):
		yt_opt['outtmpl'] = f"{path}/%(playlist_title)s/%(title)s.%(ext)s"
		try:
			with yt_dlp.YoutubeDL(yt_opt) as ydl:
				ydl.download([self.url])
				os.system('cls')
				console.print(f'[Download] ПлейЛист сохранен')
				console.input('[Action] Press: ')
		except:
			pass

class TikTok:
	def __init__(self, url):
		self.url = url

	def get_video_info(self):
		with yt_dlp.YoutubeDL(tiktok_opt_meta) as ydl:
			info = ydl.extract_info(self.url, download=False)
			
			# Форматируем дату в привычный формат
			upload_date = info.get('upload_date')
			if upload_date:
				upload_date = datetime.strptime(upload_date, '%Y%m%d').strftime('%d %B %Y')

			return {
				'title': info.get('title'),
				'id': str(info.get('id')),
				'duration': str(info.get('duration')),
				'view_count': str(info.get('view_count')),
				'like_count': str(info.get('like_count')),
				'upload_date': str(upload_date),
				'uploader': info.get('uploader'),
			}

	def download_video(self, path='./videos/TikTok'):
		new_name = f'{uuid.uuid4()}.mp4'
		tiktok_opt['outtmpl'] = f'{path}/{new_name}'
		with yt_dlp.YoutubeDL(tiktok_opt) as ydl:
			ydl.download([self.url])

		os.system('cls')
		console.print(f'[Download] видео сохранено: {path}/{new_name}')
		console.input('[Action] Press: ')

class PornHub:
	def __init__(self, url):
		self.client = phub.Client()
		self.video = self.client.get(url)

	def get_video_info(self):
		return {
			'likes': str(self.video.likes.up),
			'dislikes': str(self.video.likes.down),
			'title': self.video.title,
			'image': self.video.image,
			'duration': str(self.video.duration),
			'author': self.video.author.name,
			'views': str(self.video.views),
			'videoOBJ': self.video
		}

"""
=======Application=======
"""

class Application:
	def __init__(self):
		pass

	def welcome_screen(self):
		"""Отображение приветственного экрана с правильным выравниванием."""
		os.system("cls")
		
		# Создаем текст для панели
		text = Text("Добро пожаловать в Universal Download", style="bold green")
		sub_text = Text("Используйте это приложение с удовольствием!\n", style="dim italic")
		
		# Объединяем текст в панель
		panel = Panel(
			Text.from_markup(
				f"[bold yellow]{text}[/bold yellow]\n[dim italic]{sub_text}[/dim italic]"
			),
			border_style="bold green",
			title="Приветствие",
			subtitle="[bold cyan]Начнем работу![/bold cyan]",
		)
		
		# Выравниваем панель по центру экрана
		aligned_panel = Align.center(panel, vertical="middle")
		console.print(aligned_panel)
		sleep(3)
		os.system("cls")

	def TikTok_menu(self):
		os.system("cls")
		menu = {
			'1': 'GetVideoInfo',
			'2': 'Download video'
		}
		for key, value in menu.items():
			console.print(f"[bold cyan]{key}[/bold cyan]: {value}")
		choice = Prompt.ask("Выберите опцию", choices=list(menu.keys()), default="2")
		if choice == '1':
			url = console.input('отправьте ссылку: ')
			AppTikTok(TikTok(url), console).display_dataVideoInfo(TikTok(url).get_video_info())
		elif choice == '2':
			url = console.input('отправьте ссылку: ')
			os.system('cls')
			TikTok(url).download_video()

	def PornHub_menu(self):
		os.system('cls')
		menu = {
			'1': 'GetVideoInfo',
			'2': 'Download video',
			'3': "Download Preview Photo",
			'4': 'Exit'
		}

		for key, value in menu.items():
			console.print(f"[bold cyan]{key}[/bold cyan]: {value}")
		choice = Prompt.ask("Выберите опцию", choices=list(menu.keys()), default="2")
		if choice == '1':
			url = console.input('отправьте ссылку: ')
			AppPornHub(console=console).display_dataVideoInfo(PornHub(url).get_video_info())
		elif choice == '2':
			new_name = f'{uuid.uuid4()}.mp4'
			threads = console.input(f'[System] Отправьте количество потоков: ')

			os.system('cls')
			console.print('[System] Загрузка начата')
			data['videoOBJ'].download(path = f'./videos/PornHub/{new_name}', quality = Quality.BEST, downloader = download.threaded(max_workers = 1 if type(threads) is not int else threads, timeout = 30))
			os.system('cls')
			console.print(f'[Download] видео сохранено: ./videos/PornHub/{new_name}')
			console.input('[Action] Press: ')
		elif choice == '3':
			new_name = f'{uuid.uuid4()}.jpg'
			console.print('[System] Загрузка начата')
			data['image'].download(f'./videos/PornHub/images/{new_name}')
			console.print(f'[Download] Изображение сохранено: ./videos/PornHub/images/{new_name}')
			console.input('[Action] Press: ')

	def YouTube_menu(self):
		os.system('cls')
		menu = {
			'1': 'Get Video From Channel',
			'2': 'GetVideoInfo',
			'3': "Download Video",
			'4': 'Download Video From Channel',
			'5': 'Download PlayList',
			'6': 'Exit'
		}

		for key, value in menu.items():
			console.print(f"[bold cyan]{key}[/bold cyan]: {value}")

		choice = Prompt.ask("Выберите опцию", choices=list(menu.keys()), default="6")

		if choice == '1':
			url = console.input('отправьте ссылку: ')
			AppYouTube(YouTube(url), console).display_dataAllVideoInfo(YouTube(url).get_videos_by_channel())
		elif choice == '2':
			url = console.input('отправьте ссылку: ')
			AppYouTube(YouTube(url), console).display_dataVideoInfo(YouTube(url).get_video_info())
		elif choice == '3':
			url = console.input('отправьте ссылку на видео: ')
			YouTube(url).download_video()
		elif choice == '4':
			url = console.input('отправьте ссылку на канал: ')
			YouTube(url).download_all_video_by_channel()
		elif choice == '5':
			url = console.input('отправьте ссылку на ПлейЛист: ')
			YouTube(url).download_playlist()

	def Anime_menu(self):
		url = console.input('отправьте ссылку на аниме или на сезон: ')
		AppAnimeJutSuSite(JutSu(url), console).display_dataAnimeInfo()

	def main_menu(self):
		"""Отображение главного меню."""
		os.system("cls")
		console.print(Panel("[bold green]Меню:[/bold green]", border_style="bold cyan"))
		menu = {
			"1": "Anime(JutSu)",
			"2": "YouTube",
			"3": "TikTok",
			"4": "PornHub",
			"5": "Exit"
		}
		for key, value in menu.items():
			console.print(f"[bold cyan]{key}[/bold cyan]: {value}")

		choice = Prompt.ask("Выберите опцию", choices=list(menu.keys()), default="5")
		return choice

	def main(self):
		self.welcome_screen()
		while True:
			choice = self.main_menu()
			if choice == '1':
				self.Anime_menu()
			elif choice == '2':
				self.YouTube_menu()
			elif choice == '3':
				self.TikTok_menu()
			elif choice == '4':
				self.PornHub_menu()
			elif choice == '5':
				break

Application().main()