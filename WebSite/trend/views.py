from django.shortcuts import render

# Create your views here.

def main(request):
    return render(request,'trend.html')

#como converter o datetimefield para unix timestamp para ser utilizada no epoch
#epoch = int(time.mktime(reg.TimeStamp.timetuple())*1000)

