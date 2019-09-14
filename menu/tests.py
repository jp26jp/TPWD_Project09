from io import StringIO

from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase

from menu.forms import MenuForm
from menu.models import Menu, Item, Ingredient


class Tests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        self.ingredient = Ingredient.objects.create(name="chocolate")
        self.ingredient.save()
        self.item = Item.objects.create(
            name="Chocolate soda",
            description="Chocolate soda with a cherry on top",
            chef=self.user,
        )
        self.item.save()
        self.item.ingredients.add(self.ingredient)
        self.menu = Menu.objects.create(
            season="Fall",
            expiration_date="2020-05-31"
        )
        self.menu.save()
        self.menu.items.add(self.item)
        self.menu.save()
        self.form = MenuForm(
            data={'season': self.menu.season, 'items': [self.item], 'expiration_date': self.menu.expiration_date})

    def test_ingredient_string_representation(self):
        self.assertEqual(str(self.ingredient), self.ingredient.name)

    def test_item_string_representation(self):
        self.assertEqual(str(self.item), self.item.name)

    def test_menu_string_representation(self):
        self.assertEqual(str(self.menu), self.menu.season)

    def test_MenuForm_valid(self):
        self.assertTrue(self.form.is_valid())

    def test_menu_list_view(self):
        resp = self.client.get(reverse('menu_list'))
        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.menu, resp.context['menus'])

    def test_menu_detail_view(self):
        resp = self.client.get(reverse('menu_detail', kwargs={'pk': self.menu.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.menu, resp.context['menu'])

    def test_item_detail_view(self):
        resp = self.client.get(reverse('item_detail', kwargs={'pk': self.item.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.item, resp.context['item'])
        resp = self.client.get(reverse('item_detail', kwargs={'pk': 400}))
        self.assertEqual(resp.status_code, 404)

    def test_create_new_menu_view(self):
        form_data = {
            'season': self.menu.season,
            'items': [self.item.pk],
            'expiration_date': self.menu.expiration_date,
        }
        response = self.client.post(reverse('menu_new'), form_data)
        # get the lastest menu saved
        menu = Menu.objects.latest('id')
        self.assertRedirects(response, reverse('menu_detail', kwargs={'pk': menu.pk}))
