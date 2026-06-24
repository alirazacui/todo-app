from django.shortcuts import render, redirect, get_object_or_404

from .forms import TaskForm
from .models import Task


def task_list(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm()

    tasks = Task.objects.all()
    return render(request, 'todos/task_list.html', {'tasks': tasks, 'form': form})


def task_toggle(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.completed = not task.completed
    task.save()
    return redirect('task_list')


def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.delete()
    return redirect('task_list')
