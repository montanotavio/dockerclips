# from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from django.conf import settings
from .models import VideoClip
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from hashlib import sha256 as hasher
import time,os

# Create your views here.
def home(request):
	current_time = time.strftime('%B %-d, %Y %-I:%M:%S %p', time.localtime())
	allVideoClips = VideoClip.objects.order_by('epoch').reverse().all()
	# get files in dir
	filenames = os.listdir(settings.MEDIA_ROOT)
	# sort by modification time
	filenames.sort(key=lambda fn: os.path.getmtime(os.path.join(settings.MEDIA_ROOT, fn)), reverse=True)

	page = request.GET.get('page', 1)
	paginator = Paginator(allVideoClips, 3)
	try:
		videoClips = paginator.page(page)
	except PageNotAnInteger:
		videoClips = paginator.page(1)
	except EmptyPage:
		videoClips = paginator.page(paginator.num_pages)
	return render(request, 'home.html', {'time':current_time, 'videoClips':videoClips})

def upload(request):
	if request.method == 'POST':
		# verify correct passphrase
		salt = os.environ.get('HASH_SALT') if os.environ.get('HASH_SALT') else ''
		authPassphrase = os.environ.get('SHA256_PASS')
		passphrase = request.POST['passphrase']
		hashedPassphrase = str(hasher((str(passphrase)+str(salt)).encode('utf-8')).hexdigest())
		if not passphrase or authPassphrase != hashedPassphrase:
			return render(request, 'upload.html', {'wrong_password': True})

		# save file with unique filename from hashing
		if request.FILES['upload']:
			video = request.FILES['upload']
			title=os.path.splitext(video.name)[0]

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
			return render(request, 'upload.html', {'file_submitted': True, 'video': newVideoClip})
	return render(request, 'upload.html')

def about(request):
	return render(request, 'about.html', {})