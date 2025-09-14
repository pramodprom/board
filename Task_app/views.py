from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm

# Public board (only display tasks)

def board(request):
    tasks = {
        "todo": Task.objects.filter(status="todo"),
        "in_progress": Task.objects.filter(status="in_progress"),
        "code_review": Task.objects.filter(status="code_review"),
        "done": Task.objects.filter(status="done"),
    }
    return render(request, "Task_app/board.html", {"tasks": tasks})


# Admin page: Add & list tasks
def task_admin(request):
    tasks = Task.objects.all().order_by("-created_at")
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("task_admin")
    else:
        form = TaskForm()
    return render(request, "Task_app/task_admin.html", {"form": form, "tasks": tasks})


# Edit Task
def edit_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("task_admin")
    else:
        form = TaskForm(instance=task)
    return render(request, "Task_app/edit_task.html", {"form": form})


# Delete Task
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        task.delete()
        return redirect("task_admin")   # name from your urls.py
    return render(request, "Task_app/delete_task.html", {"task": task})


def update_task_status(request):
    if request.method == "POST":
        task_id = request.POST.get("task_id")
        new_status = request.POST.get("status")

        try:
            task = Task.objects.get(id=task_id)
            task.status = new_status
            task.save()
            return JsonResponse({"success": True})
        except Task.DoesNotExist:
            return JsonResponse({"success": False, "error": "Task not found"})
    return JsonResponse({"success": False, "error": "Invalid request"})
