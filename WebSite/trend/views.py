from django.shortcuts import render
from .models import TrendRegister
from django.http import JsonResponse

# Create your views here.

def main(request):
    return render(request,'trend.html')

#como converter o datetimefield para unix timestamp para ser utilizada no epoch
#epoch = int(time.mktime(reg.TimeStamp.timetuple())*1000)

def refresh(request):
    if request.is_ajax():
        try:
            trend_reg = TrendRegister.objects.latest('pk')
            trend_data = trend_reg.serialize()
        except Exception as err:
            trend_data = None
            print(str(err))
        finally:
            return JsonResponse(trend_data,safe=False)
    
