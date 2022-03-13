# from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from django.conf import settings
from .models import VideoClip
from hashlib import sha256 as hasher
import time,os

# Create your views here.
def home(request):
	current_time = time.strftime('%B %-d, %Y %-I:%M:%S %p', time.localtime())
	return render(request, 'home.html', {'time':current_time})

def upload(request):
	if request.method == 'POST':
		# verify correct passphrase
		salt = os.environ.get('HASH_SALT')
		authPassphrase = os.environ.get('SHA256_PASS')
		passphrase = request.POST['passphrase']
		print(f'salt is: {salt}')
		hashedPassphrase = str(hasher((str(passphrase)+str(salt)).encode('utf-8')).hexdigest())
		if not passphrase or authPassphrase != hashedPassphrase:
			print(authPassphrase)
			print(hashedPassphrase)
			return render(request, 'upload.html', {'wrong_password': True})

		# save file with unique filename from hashing
		if request.FILES['upload']:
			video = request.FILES['upload']
			title = video.name[:-4]

			# epoch given in ms, so convert to seconds
			epoch = request.POST['epoch']
			epoch = int(epoch)/1000.0

			# generate unique filename
			hash = hasher(str(epoch).encode('utf-8')).hexdigest()[:10]
			filename = f'{title}__{hash}__.mp4'
			request.FILES['upload'].name = filename

			# ensure uploaded clip is not already in database
			newVideoClip = VideoClip.objects.filter(filename=filename,epoch=epoch).first()
			if not newVideoClip:
				date = time.strftime('%B %-d, %Y %-I:%M %p', time.localtime(epoch))
				newVideoClip = VideoClip(title=title,date=date,epoch=epoch,filename=filename,file=video)
				newVideoClip.save()
				print(settings.MEDIA_ROOT)
			return render(request, 'upload.html', {'file_submitted': True, 'video': newVideoClip})
	return render(request, 'upload.html')

def about(request):
	return render(request, 'about.html', {})