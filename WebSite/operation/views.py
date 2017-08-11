from django.shortcuts import render
from .models import DataDisplay,Registers


# Create your views here.
def main(request):
    dp_col = DataDisplay.objects.all()
    print(dp_col[0].name)
    reg = Registers.objects.latest('pk')
    context = {
        'dp_col': dp_col,
        'reg':reg
    }
    return render(request,'operation.html',context)