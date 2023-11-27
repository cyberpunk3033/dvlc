
# Create your views here.
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import ClientForm
from django.shortcuts import render
from .models import Client

# Create your views here.
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('client_list')  # шаблон перехода на страницу
        else:
            error_message = 'Неверные учетные данные'
    else:
        error_message = ''

    return render(request, 'login.html', {'error_message': error_message})
def client_list(request):
    # проверяем, есть ли параметр q в запросе
    q = request.GET.get('q')
    if q:
        # если есть, то вызываем функцию client_search с этим параметром
        return client_search(request, q)
    else:
        # если нет, то получаем список всех клиентов из базы данных
        client_list = Client.objects.all()
        # передаем список клиентов в шаблон
        return render(request, 'client_list.html', {'client_list': client_list})


def client_search(request, q):
    # фильтруем список клиентов по полю name
    client_list = Client.objects.filter(name__icontains=q)
    # передаем отфильтрованный список в шаблон
    return render(request, 'client_list.html', {'client_list': client_list})
'''
def client_list(request):
# получаем список всех клиентов из базы данных
    client_list = Client.objects.all()
    # передаем список клиентов в шаблон
    return render(request, 'client_list.html', {'client_list': client_list})

def client_search(request):
# получаем значение из параметра q в запросе
    q = request.GET.get('q')
    # фильтруем список клиентов по полю name
    client_list = Client.objects.filter(name__icontains=q)
    # передаем отфильтрованный список в шаблон
    return render(request, 'client_list.html', {'client_list': client_list})
'''
def client_form(request):
# если запрос методом POST, то обрабатываем данные из формы
    if request.method == 'POST':
    # создаем объект формы и заполняем его данными из запроса
        form = ClientForm(request.POST)
    # проверяем валидность данных
        if form.is_valid():
        # сохраняем данные в базу данных
            form.save()
        # перенаправляем на страницу со списком клиентов
            return redirect('client_list')
        # если запрос методом GET, то создаем пустой объект формы
    else:
        form = ClientForm()
        # передаем объект формы в шаблон
        return render(request, 'client_form.html', {'form': form})