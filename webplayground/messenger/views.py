from django.contrib.auth.models import User
from django.http import Http404, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy

# Create your views here.
from .models import Thread, Message
from django.views.generic import DetailView, TemplateView

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


@method_decorator(login_required, name='dispatch')
class ThreadList(TemplateView):
    template_name = 'messenger/thread_list.html'


@method_decorator(login_required, name='dispatch')
class ThreadDetail(DetailView):
    model = Thread

    def get_object(self):
        obj = super(ThreadDetail, self).get_object()
        if self.request.user not in obj.users.all():
            raise Http404()
        return obj


def add_message(request, pk):
    json_response = {'created': False}
    if request.user.is_authenticated:
        content = request.GET.get('content', None)
        if content:
            thread = get_object_or_404(Thread, pk=pk)
            message = Message.objects.create(user=request.user, content=content)
            thread.messages.add(message)
            json_response['created'] = True
    else:
        raise Http404('User is no authenticated')
    return JsonResponse(json_response)


@login_required
def start_thread(request, username):
    user = get_object_or_404(User, username=username)
    thread = Thread.objects.find_or_create(user, request.user)
    return redirect(reverse_lazy('messenger:detail', args=[thread.pk]))
