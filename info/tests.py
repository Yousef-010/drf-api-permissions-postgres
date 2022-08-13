from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from .models import Book


# Create your tests here.
class BookTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        test_user1 = get_user_model().objects.create_user(
            username="test_user1", password="pass"
        )
        test_user1.save()

        test_user2 = get_user_model().objects.create_user(
            username="test_user2", password="pass"
        )
        test_user1.save()

        test_book = Book.objects.create(
            author =test_user1,
            name="test_book",
            about="testing about book",
        )
        test_book.save()

    def setUp(self):
        self.client.login(username='test_user1', password="pass")

    def test_book_model(self):
        book = Book.objects.get(id=1)
        actual_author = str(book.author)
        actual_name = str(book.name)
        actual_about = str(book.about)
        self.assertEqual(actual_author, "test_user1")
        self.assertEqual(actual_name, "test_book")
        self.assertEqual(actual_about, "testing about book")

    def test_get_book_list(self):
        url = reverse("book_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        book = response.data
        self.assertEqual(len(book), 1)
        self.assertEqual(book[0]["name"], "test_book")

    def test_auth_required(self):
        self.client.logout()
        url = reverse("book_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_only_author_can_delete(self):
        self.client.logout()
        self.client.login(username='test_user2', password="pass")
        url = reverse("book_detail", args=[1])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_book_by_id(self):
        url = reverse("book_detail", args=(1,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        food = response.data
        self.assertEqual(food["name"], "test_book")

    def test_create_book(self):
        url = reverse("book_list")
        data = {
            "author": 1,
            "name": "test_book_two",
            "about": "this is for testing",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        book = Book.objects.all()
        self.assertEqual(len(book), 2)
        self.assertEqual(Book.objects.get(id=2).name, "test_book_two")

    def test_update_book(self):
        url = reverse("book_detail", args=(1,))
        data = {
            "author": 1,
            "name": "test_book_two_updated",
            "about": "this is for testing",
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        book = Book.objects.get(id=1)
        self.assertEqual(book.name, data["name"])
        self.assertEqual(book.author.id, data["author"])
        self.assertEqual(book.about, data["about"])
