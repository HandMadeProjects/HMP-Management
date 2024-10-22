#  i have created this file - GTA



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from .models import UserData, RequestData, ProjectData  # Assuming UserData model is in the same app
from django.urls import reverse


# from django.contrib.auth.forms import UserCreationForm
# from django.views.decorators.csrf import csrf_exempt
# import uuid
# import random

# import folium

# import ast
from datetime import datetime, timedelta





@login_required
def dashboard(request):
    Proj_Data_Onhold = ProjectData.objects.filter(status="onhold")
    Proj_Data_New = ProjectData.objects.filter(status="new")
    Proj_Data_Talk =ProjectData.objects.filter(status="talk")
    Proj_Data_Progress = ProjectData.objects.filter(status="progress")
    Proj_Data_Submission = ProjectData.objects.filter(status="submission")
    Proj_Data_Done = ProjectData.objects.filter(status="done")
    Proj_Data_All = ProjectData.objects.filter()

    Req_Data_Done = RequestData.objects.filter(status="new")

    context = {
        'len_Proj_Data_Onhold':     len(Proj_Data_Onhold),
        'len_Proj_Data_Talk':       len(Proj_Data_Talk),
        'len_Proj_Data_New':        len(Proj_Data_New),
        'len_Proj_Data_Progress':   len(Proj_Data_Progress),
        'len_Proj_Data_Submission': len(Proj_Data_Submission),
        'len_Proj_Data_Done':       len(Proj_Data_Done),
        'len_Proj_Data_All':        len(Proj_Data_All),
        
        'len_Req_Data_Done':        len(Req_Data_Done),
    }
    return render(request, 'hmpapp/dashboard.html', context)



@login_required
def projects(request, myslug):
    print(f"New project page accessed with slug: {myslug}")  # Print the slug to the console/log
    if myslug == 'all':
        Proj_Data = ProjectData.objects.filter().order_by('-pub_date', '-pub_time')
    else:
        Proj_Data = ProjectData.objects.filter(status=myslug).order_by('-pub_date', '-pub_time')

    print(f"Proj_Data: {Proj_Data}")
    
    context = {
        'Proj_Data': Proj_Data,
        'lenProj_Data': len(Proj_Data),
    }
    return render(request, 'hmpapp/projects.html', context)


@login_required
def projectdetails(request, myid):
    # Fetch the project by its ID
    project = get_object_or_404(ProjectData, proj_id=myid)
    print(f"project: {project}")

    # projectRequest = RequestData.objects.filter(proj_id=myid)
    projectRequest = RequestData.objects.filter(proj_id=myid).order_by('-pub_date', '-pub_time')

    print(f"projectRequest: {projectRequest}")
    
    # Pass the project data to the context
    context = {
        'project': project,
        'projectRequest': projectRequest,
        'LenprojectRequest': len(projectRequest),
    }

    return render(request, 'hmpapp/projectdetail.html', context)





@login_required
def addproject(request):
    error_message = None
    if request.method == 'POST':
        projtitle = request.POST['projtitle']
        proj_details = request.POST['projdetails']

        print(f"projtitle: {projtitle}, proj_details: {proj_details}")

        # Get current date and time
        currentDateTime = getCurrentDateTime()
        pub_date, pub_time = currentDateTime.split(' ')  # Split into date and time

        # Create UserData instance
        ProjectData.objects.create(
            user_name=request.user.username,
            projtitle=projtitle,
            proj_details=proj_details,
            pub_date=pub_date,
            pub_time=pub_time,
        )
        return redirect('dashboard')
    
    return render(request, 'hmpapp/addproject.html', {'error_message': error_message})


@login_required
def addrequest(request):
    error_message = None
    if request.method == 'POST':
        reqtitle = request.POST['reqtitle']
        req_details = request.POST['req_details']
        projectid = request.POST['projectid']

        print(f"reqtitle: {reqtitle}, req_details: {req_details}")

        # Get current date and time
        currentDateTime = getCurrentDateTime()
        pub_date, pub_time = currentDateTime.split(' ')  # Split into date and time

        # Create UserData instance
        RequestData.objects.create(
            user_name=request.user.username,
            reqtitle=reqtitle,
            req_details=req_details,
            pub_date=pub_date,
            pub_time=pub_time,
            proj_id=projectid,
        )
        return redirect('dashboard')

    activeProjects = ProjectData.objects.exclude(status='done')


    return render(request, 'hmpapp/addrequest.html', 
    {'error_message': error_message, 'activeProjects': activeProjects})




@login_required
def request_view(request, myslug):
    print(f"New project page accessed with slug: {myslug}")  # Print the slug to the console/log
    if myslug == 'all':
        projectRequest = RequestData.objects.filter().order_by('-pub_date', '-pub_time')
    else:
        projectRequest = RequestData.objects.filter(status=myslug).order_by('-pub_date', '-pub_time')

    print(f"projectRequest: {projectRequest}")

    # Pass the project data to the context
    context = {
        'projectRequest': projectRequest,
        'LenprojectRequest': len(projectRequest),
    }
    return render(request, 'hmpapp/request.html', context)


@login_required
def updateRequestStatus(request, req_id, new_status):
    # Fetch the request by its ID
    request_data = get_object_or_404(RequestData, req_id=req_id)
    print(f"new_status: {new_status}")
    
    # Update the status field
    request_data.status = new_status
    request_data.save()  # Save the changes to the database

    # Redirect to the project details page or any other desired page
    return HttpResponseRedirect(reverse('projectdetails', args=[request_data.proj_id]))




@login_required
def account(request):
    # print(f"request.user.username: {request.user.username}")
    user_data = UserData.objects.filter(user_name=request.user.username).first()
    # print(f"user_data: {user_data}")
    
    context = {
        'user_data': user_data,
    }
    return render(request, 'hmpapp/account.html', context)









def user_register(request):
    error_message = None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        role = request.POST['role']

        # Check if the username is unique
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(username=username, password=password, email=email)

            # Get current date and time
            currentDateTime = getCurrentDateTime()
            pub_date, pub_time = currentDateTime.split(' ')  # Split into date and time

            # Create UserData instance
            UserData.objects.create(
                user_name=username,
                pub_date=pub_date,
                pub_time=pub_time,
                role=role
            )
            return redirect('user_login')
        else:
            error_message = 'Username already exists'
    
    return render(request, 'hmpapp/register.html', {'error_message': error_message})

def user_login(request):
    error_message = None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Adjust to your actual view name
        else:
            error_message = 'Invalid username or password'

    return render(request, 'hmpapp/login.html', {'error_message': error_message})

def user_logout(request):
    logout(request)
    return redirect('user_login')  # Redirect to your login view




# Custome Functions:

def getCurrentDateTime() -> str:
    """
    Get the current date and time in the format 'YYYY-MM-DD HH:MM:SS'.
    
    Returns:
        str: Current date and time as a formatted string.
    """
    currentDateTime = datetime.now()
    return currentDateTime.strftime('%Y-%m-%d %H:%M:%S')





# def dashboard(request):
#     return render(request, 'hmpapp/dashboard.html')

# def projects(request):
#     return render(request, 'hmpapp/projects.html')

# def account(request):
#     return render(request, 'hmpapp/account.html')

# def projectdetails(request):
#     return render(request, 'hmpapp/projectdetail.html')

# def request(request):
#     return render(request, 'hmpapp/request.html')