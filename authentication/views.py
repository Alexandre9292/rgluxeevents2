from django.shortcuts import render

#Chargement de la page de mention légales
def mentions_legales(request):
    return render(request, 'authentication/mentions_legales.html')
