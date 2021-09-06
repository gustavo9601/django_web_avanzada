from django.test import TestCase
from django.contrib.auth.models import User
from .models import Thread, Message


# Create your tests here.
class ThreadTestCase(TestCase):

    # Para cada test se ejecuta el setUp
    def setUp(self):
        self.user_1 = User.objects.create_user('user1', None, 'Pruebas1234')
        self.user_2 = User.objects.create_user('user2', None, 'Pruebas1234')
        self.user_3 = User.objects.create_user('user3', None, 'Pruebas1234')

        self.thread = Thread.objects.create()

    def test_add_users_to_thread(self):
        self.thread.users.add(self.user_1, self.user_2)
        # Comprobando si hay dos usuarios en la lista, para el thread creado
        self.assertEqual(len(self.thread.users.all()), 2)

    def test_filter_thread_by_users(self):
        self.thread.users.add(self.user_1, self.user_2)
        threads = Thread.objects.filter(users=self.user_1).filter(users=self.user_2)
        self.assertEqual(self.thread, threads[0])

    def test_filter_non_existent_thread(self):
        threads = Thread.objects.filter(users=self.user_1).filter(users=self.user_2)
        # Comprobando que no existen ningun thread
        self.assertEqual(len(threads), 0)

    def test_add_message_to_thread(self):
        self.thread.users.add(self.user_1, self.user_2)
        message_1 = Message.objects.create(user=self.user_1, content='Saludo 1')
        message_2 = Message.objects.create(user=self.user_2, content='Saludo 2')
        self.thread.messages.add(message_1, message_2)
        # Verificando que se hallan añadiddo 2 mensajes al hilo
        self.assertEqual(len(self.thread.messages.all()), 2)

        for message in self.thread.messages.all():
            print(f"({message.user}: {message.content})")

    def test_add_message_from_user_not_in_thread(self):
        self.thread.users.add(self.user_1, self.user_2)
        message_1 = Message.objects.create(user=self.user_1, content='Saludo 1')
        message_2 = Message.objects.create(user=self.user_2, content='Saludo 2')
        message_3 = Message.objects.create(user=self.user_3, content='Saludo 3')
        self.thread.messages.add(message_1, message_2, message_3)
        # Verificando que se hallan añadiddo 2 mensajes al hilo
        self.assertEqual(len(self.thread.messages.all()), 2)

    def test_find_thread_with_custom_manager(self):
        self.thread.users.add(self.user_1, self.user_2)
        # usa find funcion propia del modelo
        thread = Thread.objects.find(self.user_1, self.user_2)
        self.assertEqual(self.thread, thread)

    def test_find__or_create_thread_with_custom_manager(self):
        self.thread.users.add(self.user_1, self.user_2)
        # usa find funcion propia del modelo
        thread_1 = Thread.objects.find_or_create(self.user_1, self.user_2)
        thread_2 = Thread.objects.find_or_create(self.user_1, self.user_3)
        self.assertIsNotNone(thread_1)
        self.assertIsNotNone(thread_2)
