# VIEWS
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

from .forms import ClientForm, CalculationForm
from .models import Client,Calculation
from django.views.generic import ListView, DetailView, UpdateView
from rest_framework import generics

from .serializers import CalculationSerializer

# region ЛОГИН
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


# endregion

# region КОНТРАГЕНТЫ
def client_list(request):
    """
    Весь список клиентов
    :param request:
    :return:
    """
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
    """
    Функция поиска клиентов
    :param request:
    :param q:
    :return:
    """
    # фильтруем список клиентов по полю name
    client_list = Client.objects.filter(name__icontains=q)
    # передаем отфильтрованный список в шаблон
    return render(request, 'client_list.html', {'client_list': client_list})


# TODO: автоматизировать подстановку пользователя при добавлении клиента
def client_form(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)  # Не сохраняем форму сразу
            client.user = request.user  # Устанавливаем поле user равным текущему пользователю
            client.save()  # Сохраняем форму
            return redirect('client_list')

    else:
        form = ClientForm()

        return render(request, 'client_form.html', {'form': form})


# TODO: НАСТРОИТЬ ПРАВА НА УДАЛЕНИЕ ИЗМЕНЕНИЕ КОНТРАГЕНТОВ

def client_edit(request, pk):
    """
    Изменение данных контрагента по
    первичному ключу при выборе в списке
    :param request:
    :param pk:
    :return:
    """
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('client_list')
    else:
        form = ClientForm(instance=client)
        return render(request, 'client_edit.html', {'form': form})



# region РАСЧЕТЫ

class CalculationListView(ListView):
    model = Calculation
    template_name = 'calculation_list.html'
    context_object_name = 'calculations'
    paginate_by = 10  #
class CalculationDetailView(DetailView):
    model = Calculation
    template_name = 'calculation_detail.html'
    context_object_name = 'calculation'

def calculation_edit(request, pk):
    """
    Изменение данных контрагента по
    первичному ключу при выборе в списке
    :param request:
    :param pk:
    :return:
    """
    calculation = get_object_or_404(Calculation, pk=pk)
    if request.method == 'POST':
        form = CalculationForm(request.POST, instance=calculation)
        if form.is_valid():
            form.save()
            return redirect('calculation_list')
    else:
        form = CalculationForm(instance=calculation)
        return render(request, 'calculation_detail.html', {'form': form})

# endregion

def search_clients(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        query = request.GET.get('query', '')
        clients = Client.objects.filter(name__icontains=query)

        data = [{'id': client.id, 'name': client.name} for client in clients]
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({}, status=400)





class CalculationCreateView(generics.CreateAPIView):
    queryset = Calculation.objects.all() # набор объектов для проверки уникальности
    serializer_class = CalculationSerializer # сериализатор для ввода и вывода данных
# endregion