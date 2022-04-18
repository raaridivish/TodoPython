from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .models import Task
from .forms import TodoForm
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, DeleteView


# Create your views here.
# def index(request):
#     return HttpResponse("Hello i'm index page")


# def home(request):
#     tasks=Task.objects.all()
#     task_list={'tasklist':tasks}
#     return render(request, "home.html", task_list)


class Tasklistview(ListView):
    model = Task
    template_name = 'home.html'
    context_object_name = 'task'

    def post(self, request, *args, **kwargs):
        object = self.get_object()
        request.session['selected_transcript'] = object.id
        return redirect('cbvhome')


class Taskdetailview(DetailView):
    model = Task
    template_name = 'detailview.html'
    context_object_name = 'task'


class Taskupdateview(UpdateView):
    model = Task
    template_name = 'update.html'
    context_object_name = 'task'
    fields = ['name', 'priority', 'date']

    def get_success_url(self):
        return reverse_lazy('cbvdetail', kwargs={'pk': self.object.id})


class Taskdeleteview(DeleteView):
    model = Task
    template_name = 'delete.html'
    success_url = reverse_lazy('cbvhome')


def add(request):
    task_list = Task.objects.all()
    if request.method == 'POST':
        name = request.POST.get('taskname', '')
        priority = request.POST.get('priority', '')
        date = request.POST.get('date', '')
        task = Task(name=name, priority=priority, date=date)
        task.save()
    return render(request, 'home.html', {'task': task_list})


def details(request):
    task = Task.objects.all()
    return render(request, 'detail.html', {'task': task})


def delete(request, taskid):
    task = Task.objects.get(id=taskid)
    if request.method == 'POST':
        task.delete()
        return redirect('/')
    return render(request, 'delete.html')


def update(request, id):
    t = Task.objects.get(id=id)
    f = TodoForm(request.POST or None, instance=t)
    if f.is_valid():
        f.save()
        return redirect('/')
    return render(request, 'edit.html', {'f': f, 'task': t})
