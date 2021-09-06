from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import m2m_changed


# Create your models here.
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']


class ThreadManager(models.Manager):
    def find(self, user_1, user_2):
        """
            Dentro de un modelManager
            self => Thread.objects
        """
        queryset = self.filter(users=user_1).filter(users=user_2)
        if len(queryset) > 0:
            return queryset[0]
        return None

    def find_or_create(self, user_1, user_2):
        """
            Dentro de un modelManager
            self => Thread.objects
        """
        thread = self.find(user_1, user_2)
        if thread is None:
            thread = Thread.objects.create()
            thread.users.add(user_1, user_2)
        return thread


class Thread(models.Model):
    # Relaciones
    users = models.ManyToManyField(User, related_name='threads')
    messages = models.ManyToManyField(Message, related_name='threads')

    # Especificando los nuevos metodos que se extenderan del modelo
    objects = ThreadManager()


def messages_changed(sender, **kwargs):
    instance = kwargs.pop('instance', None)
    action = kwargs.pop('action', None)
    pk_set = kwargs.pop('pk_set', None)
    print("** Signal messages_changed", instance, action, pk_set)

    false_pk_set = set()
    if action is 'pre_add':
        print("**pk_set", pk_set)
        for msg_pk in pk_set:
            msg = Message.objects.get(pk=msg_pk)
            # Verificando si el usuario no esta dentro de la instancia enviada del thread
            if msg.user not in instance.users.all():
                false_pk_set.add(msg_pk)
                print(f"**Ups, {msg.user} no forma parte del thread")
    # Busca los mensajes de false_pk_set que no estan en pk_set y los borra de pk_set
    pk_set.difference_update(false_pk_set)


# Enlazando la señal de otra forma
m2m_changed.connect(messages_changed, sender=Thread.messages.through)
