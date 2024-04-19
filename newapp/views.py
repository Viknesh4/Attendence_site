import requests
import json
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

def slogin(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('student_data')  # Redirect to home page after successful login
    else:
        form = AuthenticationForm()
    return render(request, 'slogin.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('firebase_data')  # Redirect to home page after successful login
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})
@login_required
def firebase_data_view(request):
    # Firebase Realtime Database URL
    firebase_url = 'https://attendance-db-20da7-default-rtdb.firebaseio.com/students.json'

    # Make GET request to Firebase Realtime Database
    response = requests.get(firebase_url)

    # Check if request was successful
    if response.status_code == 200:
        firebase_data = response.json() 
        students_data = firebase_data 
    
        return render(request, 'firebase.html', {'students_data': students_data})
    else:
        error_message = "Failed to fetch data from Firebase"
        return render(request, 'error.html', {'error_message': error_message})

@login_required
def student_data(request):
    current_user = request.user

    if current_user.is_authenticated:
        username = current_user.username

    firebase_url = 'https://attendance-db-20da7-default-rtdb.firebaseio.com/students.json'
    # Make GET request to Firebase Realtime Database
    response = requests.get(firebase_url)
    # Check if request was successful
    if response.status_code == 200:
        firebase_data = response.json() 
        students_data = firebase_data 


        if username in students_data:
            status='Present'
            date = students_data[username]
            return render(request,'student_data.html',{'status':status,'date':date,'username':username})
        else:
            status='Absent'
            return render(request,'student_data.html',{'username':username,'status':status})
    else:
        error_message = "Failed to fetch data from Firebase"
        return render(request, 'error.html', {'error_message': error_message})

def index(request):
    return render(request,'index.html')