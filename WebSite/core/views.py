from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,'home.html')

#como converter o datetimefield para unix timestamp para ser utilizada no epoch
#epoch = int(time.mktime(reg.TimeStamp.timetuple())*1000)

