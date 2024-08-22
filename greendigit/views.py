from django.shortcuts import render, redirect
 
def index(request):
    if request.user.is_authenticated:
        if request.user.is_farmer:
            return redirect('farmer_dashboard')
        elif request.user.is_consumer:
            return redirect('consumer_dashboard')
    else:
        return render(request, 'index.html')
