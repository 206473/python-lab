from django.core.management.base import BaseCommand, CommandError
from Login.models import User
from main.views import get_image_size
from main.models import Subscriptions
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
from main.models import Images
class Command(BaseCommand):
	help = 'Adding new pictures'

	def handle(self, *args, **options):
		for subs in Subscriptions.objects.all():
			resp = requests.get(subs.url)
			print(subs.id)
			
			soup = BeautifulSoup( resp.content ,"html5lib")
			images = soup.find_all( 'img' )
			
			for img in images:
				width, height = get_image_size(img.get( 'src' ))
				if width>200 and height>200:
					try:
						Images.objects.create(subscribe_id=subs.id,url=img.get('src'))
					except:
						self.stdout.write('Error!')
						continue
		self.stdout.write('Successfully added')
	
	def get_image_size(url):
		try:
			data = requests.get(url).content
		except:
			try:
				data = requests.get("http:"+url).content
			except:
				return 0,0
		im = Image.open(BytesIO(data))	
		return im.size