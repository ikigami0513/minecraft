import subprocess
import os
import json
from django.http import JsonResponse
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
            return render(request, 'client/users/login.html', {
                'error_message': 'Invalid login',
            })
        
class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('index')
    
class Server(View):
    def is_server_running(self):
        process = subprocess.Popen(['ps', 'aux'], stdout=subprocess.PIPE)
        output, _ = process.communicate()
        return b'run.sh' in output

    def get(self, request):
        context = {
            'server_status': self.is_server_running()
        }
        return render(request, 'client/server/index.html', context=context)
    
    def post(self, request):
        if not os.path.exists('/minecraft/run.sh'):
            context = {
                'error': 'Le fichier de mise en route du serveur n\'existe pas.',
            }

        else:
            data = json.loads(request.body)
            action = data.get('action')

            if action == "start":
                if self.is_server_running():
                    context = {
                        'error': 'Le serveur est déjà en cours d\'exécution.',
                    }
                else:
                    command = 'cd /minecraft && sudo ./run.sh'
                    subprocess.Popen(command, shell=True)
                    context = {
                        'success': 'Le serveur a bien démarré.',
                    }

            elif action == "stop":
                if not self.is_server_running():
                    context = {
                        'error': 'Le serveur est déjà à l\'arrêt.',
                    }
                else:
                    run_command = 'cd /minecraft && sudo ./run.sh'
                    process = subprocess.Popen(run_command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
                    command = 'stop'
                    sortie, erreur = process.communicate(command.encode())
                    context = {
                        'success': 'Le serveur a bien été stoppé.'
                    }

            else:
                context = {
                    'error': 'L\'action demandée n\'est pas valide.',
                }
        
        return JsonResponse(context)