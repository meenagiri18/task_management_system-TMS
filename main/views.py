import re
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import PasswordChangeForm
from datetime import datetime

# Create your views here.
@login_required(login_url='log_in')
def home(request):
    data=Create_task.objects.filter(is_completed=False,isDelete=False)
    total_count=Assign_task.objects.filter(is_deleted=False, is_completed=False,assigned_by=request.user).count()
    completed_count=Create_task.objects.filter(is_completed=True,user=request.user).count()
    current_count=Create_task.objects.filter(is_completed=False, isDelete=False).count()
    return render(request, 'html/home.html',{'data':data,'total_count':total_count,'completed_count':completed_count,'current_count':current_count})

def base(request):
    return render(request,'base.html',{'user_name':request.user})
def log_in(request):
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')
        
        if not User.objects.filter(username=username).exists():
            messages.error(request, 'Username is not registered.')
            return redirect('log_in')
        user=authenticate(username=username, password=password)

        if user is not None:
            login(request,user)
            if remember_me:
                request.session.set_expiry(1200000)
            else:
                request.session.set_expiry(0)
            messages.success(request,"Login successfully!")
            return redirect('home')
        else:
            messages.error(request,"Invalid password")
            return redirect('log_in')
            
    return render(request,'auth/login.html')

def register(request):
    if request.method=='POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        email=request.POST['email']
        username=request.POST['username']
        password=request.POST['password']
        password1=request.POST['password1']

        if password==password1:
            try:
                 validate_password(password)
                 if User.objects.filter(username=username).exists():
                    messages.error(request, "Username already exists")
                    return redirect('register')
                 elif User.objects.filter(email=email).exists():
                    messages.error(request, "Email already exists")
                    return redirect('register')
                 elif username.lower() in password.lower():
                     messages.error(request,"Password cannot be too similar to username.")
                     return redirect('register')
                 elif not re.search(r'[A-Z]',password):
                    messages.error(request,"Password must contain atleast one uppercase letter.")
                    return redirect('register')
                 elif not re.search(r'\d', password):
                     messages.error(request, "Password must contain atleast one digit.")
                     return redirect('register')
                 elif not re.search(r'[@#%$<>]', password):
                     messages.error(request, "Password must contain atleast one special character.")
                     return redirect('register')
                 
                 else:
                   User.objects.create_user(first_name=first_name, last_name=last_name,email=email,username=username,password=password)
                   messages.success(request, "Registered successfully!")
                   return redirect('log_in')
                 
            except ValidationError as e:
                for error in e.messages:
                    messages.error(request,error)
                return redirect('register')

           
        else:
            messages.error(request,"Your passwords doesn't match")
            return redirect('register')

    return render(request,'auth/register.html')

def change_password(request):
    form = PasswordChangeForm(user=request.user)
    if request.method=='POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('log_in')

    return render(request, 'auth/change_password.html', {'form':form})

def log_out(request):
    logout(request)
    return redirect('log_in')
#  create task section start
def create(request):
    if request.method == 'POST':
        title=request.POST['title']
        description=request.POST['description']
        status=request.POST['status']
        sdate=request.POST['sdate']
        edate=request.POST['edate']
        Create_task.objects.create(title=title,description=description,status=status,start_date=sdate,end_date=edate)
        messages.success(request,"Your task is created successfully!!")
        return redirect('home')

    return render(request,'html/create.html')
#  create task section end

def view(request):
    data=Create_task.objects.filter(is_completed=False,isDelete=False)
    if request.method == 'POST':
        sort_by=request.POST.get('sort_by')
        if sort_by:
            sort_by = sort_by.strip() 
            data=data.order_by(sort_by)
        
    return render (request,'html/show.html',{'data':data})
def edit(request, id):
    data = Create_task.objects.get(id=id)
    
    if request.method == 'POST':
        data.title = request.POST["title"]
        data.description = request.POST["description"]
        data.status = request.POST["status"]
        data.sdate = request.POST["sdate"]
        data.edate = request.POST["edate"]
        data.save()
        return redirect('home')  
    
   
    return render(request, 'html/edit.html', {'data': data})

def delete_data(request,id):
    data=Create_task.objects.get(id=id)
    data.delete()
    data.delete_time=datetime.now()
    data.isDelete=True
    data.save()
    return redirect("home")

def assign(request):
    if request.method =='POST':
        title=request.POST.get('title')
        description=request.POST.get('description')
        status=request.POST.get('status')
        username=request.POST.get('user')
        ddate=request.POST.get('ddate')
        assigned_by = request.user

        if User.objects.filter(username=username).exists():
           user1=User.objects.get(username=username)#to whom task is assigned
           user2=User.objects.get(username=assigned_by)#user assigning the task
            

           Assign_task.objects.create(title=title,description=description,status=status,assign_to=user1,ddate=ddate,assigned_by=user2)
           messages.success(request,'Task is assign successfully!!')
           return redirect('home')
        else:
            messages.error(request, "Username doesnot exists!")
            return redirect('assign_task')
    return render(request,'html/assign.html')

def assigned_task(request):
    data=Assign_task.objects.filter(is_completed=False)

    return render(request,'html/assigned.html',{'data':data})
def completed(request,id):
    data=Assign_task.objects.get(id=id)
    data.is_completed=True
    data.save()
    messages.success(request,"Your task has been marked completed!")
    return redirect('assigned_task')

def current_completed(request,id):
    current_completed=Create_task.objects.get(id=id)
    current_completed.is_completed=True
    current_completed.save()
    messages.success(request,"Your task has been marked completed!")
    return redirect('view_task')

def completed_tasks(request):
    current_data = Create_task.objects.filter(is_completed=True, isDelete=False) 
    assign_data = Assign_task.objects.filter(is_deleted=False,assigned_by=request.user)  
    
    return render(request, 'html/complete.html', {'data1': current_data, 'data2': assign_data})


def clear_data(request):
    Create_task.objects.all().update(isDelete=True)
    return redirect('view_task')


#-----recycle section starts----#
def recycle(request):
    data=Create_task.objects.filter(isDelete=True)
    return render(request,'html/recycle.html',{'data':data})
#------recycle section ends----#
#------restore section starts----#
def restore(request,id):
    data=Create_task.objects.get(id=id)
    data.isDelete= False
    data.save()
    messages.success(request,"Your data has been restored successfully!")
    return redirect('recycle')
#------restore section ends----#

def delete_assign(request,id):
    assign_delete=Assign_task.objects.get(id=id)
    assign_delete.is_deleted=True
    assign_delete.delete_time=datetime.now()
    assign_delete.save()
    return redirect('completed_tasks')

def delete_current(request,id):
    current_delete=Create_task.objects.get(id=id)
    current_delete.isDelete=True
    current_delete.delete_time=datetime.now()
    current_delete.save()
    return redirect('completed_tasks')
