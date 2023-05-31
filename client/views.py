from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View

class Index(View):
    def get(self, request):
        return render(request, 'client/index.html')

class Login(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('index')
        
        return render(request, 'client/users/login.html')
    
    def post(self, request):
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'client/user/login.html', {
                'error_message': 'Invalid login',
            })
        
class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('index')
    
class Server(View):
    def get(self, request):
        return render(request, 'client/server/index.html')