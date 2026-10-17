from django.shortcuts import render

def dashboard(request):
    # This tells Django to load the HTML file we just created
    return render(request, 'core/dashboard.html')
