from django.shortcuts import render, redirect, get_object_or_404
from .models import Todo
from .forms import TodoForm
import requests 

def analyze_sentiment(text):
    try:
        headers = {
            'x-api-key': 'asdfghkl_66_zxcvbnm',  # Fixed typo
            'Content-Type': 'application/json'          # Fixed content type
        }
        
        response = requests.post(
            'http://127.0.0.1:8080/analyze',
            json={'text': text},
            headers=headers
        )

        if response.status_code == 200:
            return response.json().get('sentiment', 'Unknown')
        else:
            error = response.text
            print("API Error:", error)  # Helpful for debugging
            return "API Error"
        
    except Exception as e:
        print("Exception:", e)
        return 'API is not available.'


def todo_list(request):
    todos = Todo.objects.all()
    for todo in todos:
        todo.sentiment = analyze_sentiment(todo.description)
    return render(request,'todo/todo_list.html', {'todos': todos})

def todo_create(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.sentiment = analyze_sentiment(todo.description)
            form.save()
            return redirect('todo_list')
    else:
        form = TodoForm()
    return render(request, 'todo/todo_add.html', {'form': form})

def todo_edit(request, pk):
    todo = get_object_or_404(Todo, pk = pk)
    if request.method == 'POST':
        form = TodoForm(request.POST or None, instance=todo)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.sentiment = analyze_sentiment(todo.description)
            form.save()
            return redirect('todo_list')
    else:
        form = TodoForm(instance = todo)
    
    return render(request, 'todo/todo_edit.html', { 'form':form } )

def todo_delete(request, pk):
    todo = get_object_or_404(Todo, pk = pk)
    if request.method == 'POST':
        todo.delete()
        return redirect('todo_list')
    return render(request, 'todo/todo_delete.html', {'todo': todo})
