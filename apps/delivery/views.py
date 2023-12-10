# VIEWS
from django.contrib.auth import authenticate, login
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.html import format_html

from .forms import ClientForm, CalculationForm
from .models import Client, Calculation, BaseChain, Country
from django.views.generic import ListView, DetailView
import json

from django.http import JsonResponse, HttpResponse


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
        return render(request, 'client/client_list.html', {'client_list': client_list})


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
    return render(request, 'client/client_list.html', {'client_list': client_list})


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

        return render(request, 'client/client_form.html', {'form': form})


# TODO: НАСТРОИТЬ ПРАВА НА УДАЛЕНИЕ ИЗМЕНЕНИЕ КОНТРАГЕНТОВ
# TODO: ДОБАВИТЬ ВИДИМОСТЬ РАСЧЕТОВ НА СТРАНИЦЕ КОНТРАГЕНТА
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
        return render(request, 'client/client_edit.html', {'form': form})



# endregion

# region РАСЧЕТЫ

class calc_list_view(ListView):
    model = Calculation
    template_name = 'calculation/calculation_list.html'
    context_object_name = 'calculations'
    paginate_by = 10
    ordering = '-created'

def autocomplete(request):
    if 'term' in request.GET:
        qs = Country.objects.filter( name__icontains=request.GET.get('term'))
        countrys = list()
        for country in qs:
            countrys.append(country.name)
        # titles = [product.title for product in qs]
        return JsonResponse(countrys, safe=False)
    return render(request, 'core/home.html')

class calc_list_detail_view(DetailView):
    model = Calculation
    template_name = 'calculation/calculation_detail.html'
    context_object_name = 'calculation'





def calc_list_create_view(request):
    if request.method == 'POST':
        form = CalculationForm(request.POST)
        if form.is_valid():
            calculation = form.save(commit=False)  # Не сохраняем форму сразу
            calculation.user = request.user  # Устанавливаем поле user равным текущему пользователю
            calculation.save()  # Сохраняем форму
            return redirect('calculation-list')

    else:
        form = CalculationForm()

        return render(request, 'calculation/calculation_create.html', {'form': form})


# endregion

# EXAMPLE search

def search_view(request):
    all_people = Person.objects.all()
    context = {'count': all_people.count()}
    return render(request, 'search.html', context)

def search_client_view(request):
    all_client = Client.objects.all()
    context = {'count': all_client.count()}
    return render(request, 'search.html', context)

def search_client_results_view(request):
    query = request.GET.get('search', '')
    print(f'{query = }')

    all_client = Client.objects.all()
    if query:
        client_ = all_client.filter(name__icontains=query)
        highlighted_client = [{'name': highlight_matched_text(client.name, query)} for client in client_]
    else:
        highlighted_client = []

    context = {'client': highlighted_client, 'count': all_client.count()}
    return render(request, 'search_results.html', context)


def highlight_matched_text(text, query):
    """
    Inserts html around the matched text.
    """
    start = text.lower().find(query.lower())
    if start == -1:
        return text
    end = start + len(query)
    highlighted = format_html('<span class="highlight">{}</span>', text[start:end])
    return format_html('{}{}{}', text[:start], highlighted, text[end:])

# endregion