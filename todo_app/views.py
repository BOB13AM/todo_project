import json
import googletrans
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from googletrans import Translator

from .models import *


def index(request):
     # Authenticated users view their home page
    if request.user.is_authenticated:
        return render(request, "todo_app/index.html")

    # Everyone else is prompted to sign in
    else:
        return HttpResponseRedirect(reverse("login"))

@csrf_exempt
@login_required
def content(request):
    #get the current user 
    current_user = User.objects.get(pk=request.user.id)
    
    if current_user.is_staff:
        user_all = User.objects.filter(is_staff=False)
        return JsonResponse([content.serialize() for content in user_all], safe=False)
    else:
        user_content = current_user.tasks.all()
        return JsonResponse([content.serialize() for content in user_content], safe=False)

@csrf_exempt
@login_required
def update (request,taskid):
    if request.method=="PUT":
        #get the exact todo-task that we need to update its translated field in the task model
        target_task = task.objects.get(pk=taskid)

        #to be able to access the variables inside the body that we sent from the JS 
        data = json.loads(request.body)
        #get the value of the variable
        if data.get("translate") is not None:
            #get the translated field from task model and update its value to true
            target_task.translated = data["translate"]
        #save the change    
        target_task.save()
        #returning that the process was successful
        return JsonResponse({"message": "Task updated successfully."}, status=201)

@csrf_exempt
@login_required
def create(request):
    if request.method=="POST":
        #get the current user 
        current_user = User.objects.get(id=request.user.id)
        
        data = json.loads(request.body)
        #get the new task from user
        new_task = data.get("task", "")

        #check if i am receiving the values from the user and add the new task to the model
        if new_task and current_user:
            add_task = task(user=current_user,body=new_task)
            add_task.save()
            return JsonResponse({"message": "Task Added successfully."}, status=201)
        else:
            return JsonResponse({"error": "Missing Info"}, status=400)

@csrf_exempt
@login_required
def translation(request,target_content):
        #creating a translator object of the Translator class
        translator = Translator()
        #passing the content to the translate method(accessing this method by the translator) in the Translator class 
        result = translator.translate(target_content, dest='tl')
        #get the result text only and put it in a variable
        new_content = result.text
        #returning the translated text     
        return JsonResponse([new_content], safe=False)

@csrf_exempt
@login_required
def userpage(request,userid):
    #get the specific user from the user model
    target_user = User.objects.get(id=userid)
    #get all the user history from task model
    user_content = target_user.tasks.all()

    return JsonResponse([all_content.serialize() for all_content in user_content], safe=False)



def login_view(request):
    #check for method if its post 
    if request.method=="POST":
        # get the values of the user name and password from user
        username = request.POST.get('username')
        password = request.POST.get('password')

        #using the built-in authenticate function to check if the user name and password are the same 
        user = authenticate(request, username=username, password=password)

        #checking if the user var is not none to login the user
        if user is not None:
            login(request,user)
            return HttpResponseRedirect(reverse("index"))
        #else if the user var is none reload the login page with error message
        else:
            return render(request, "todo_app/login.html",{
                    "message": "Invalid email and/or password."
                })
    #GET method rendering the login page     
    else:
        return render(request, "todo_app/login.html")

def logout_view(request):
    #using the logout function to logout current user then redirect the user to login page  
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        # get the values of the user name and password and confirm from user
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm = request.POST.get('confirmation')
        email=request.POST.get('email')
        #creating empty email to fillup the User Class Model if the user didnt provide one
        if not email:    
            email='not provided'
        
        #check if the password and the confirmation is the same 
        if password != confirm:
            return render(request, "todo_app/register.html",{
                    "message": "Passwords must match."
                }) 
        #trying to create a new user 
        try:
            user = User.objects.create_user(username,email,password)
            user.save()
        #catching the except integrity error in case the user already exists
        except IntegrityError: 
             return render(request, "todo_app/register.html", {
                "message": "Username already taken."
            })   
        
        #login the user with the login function after creating and then redirecting to index(mainpage)
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    
    #GET Method  rendering the register page
    else:        
        return render(request, "todo_app/register.html")