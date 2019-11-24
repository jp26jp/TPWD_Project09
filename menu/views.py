from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import FormView

from .models import *
from .forms import *


def menu_list(request):
    menus = Menu.objects.filter(expiration_date__gte=timezone.now()).order_by('expiration_date').prefetch_related(
        'items')
    return render(request, 'menu/list_all_current_menus.html', {'menus': menus})


def menu_detail(request, pk):
    menu = Menu.objects.get(pk=pk)
    return render(request, 'menu/menu_detail.html', {'menu': menu})


def item_detail(request, pk):
    try:
        item = Item.objects.get(pk=pk)
    except ObjectDoesNotExist:
        raise Http404
    return render(request, 'menu/detail_item.html', {'item': item})


class CreateNewMenuFormView(FormView):
    form_class = MenuForm
    template_name = 'menu/new.html'

    def get(self, request, *args, **kwargs):
        form = MenuForm()
        return render(request, 'menu/new.html', {'form': form})

    def form_valid(self, form):
        menu = form.save()
        return redirect('menu_detail', pk=menu.pk)


def edit_menu(request, pk):
    menu = get_object_or_404(Menu, pk=pk)
    menu_form = MenuForm(instance=menu)
    if request.method == "POST":
        menu_form = MenuForm(request.POST, instance=menu)
        if menu_form.is_valid():
            menu_form.save()
    return render(request, 'menu/change_menu.html', {'menu_form': menu_form})
