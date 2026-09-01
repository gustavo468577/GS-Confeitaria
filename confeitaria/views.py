from django.shortcuts import render


# Mostra a tela inicial do sistema.
def inicio(request):
    return render(request, 'confeitaria/inicio.html')