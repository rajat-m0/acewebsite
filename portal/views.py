from django.contrib import messages
import json
import requests
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers
from django.core.files.storage import default_storage
from django.db.models import F
from django.shortcuts import render, redirect
from django.utils.timezone import localtime, now
from ace.settings import SELECTION_START_DATE, SELECTION_END_DATE, MEDIA_ROOT, SELECTION_RESULT_DATE
from portal.models import Task, Submission, Category
from users.models import Profile
from review.models import SelectionResult

import os
from .drive import upload_drive_task, create_folder, refresh_token
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
import threading
DATETIME_FORMAT = '%Y-%m-%d %H-%M-%S'


def landing(request):
    if request.user and request.user.is_authenticated:
        if Profile.objects.filter(user=request.user).exists():
            return redirect('portal_home')
        # else:
        #     return redirect('user_signup')
    return render(request, 'portal/Landing Screen/index.html')

@login_required(login_url='user_login')
def serve_tasks(request, id):
    try:
        category = Category.objects.get(pk=id)
    except ObjectDoesNotExist:
        return redirect('portal_home')
    today = localtime(now())
    if ((today < SELECTION_START_DATE) or (today > SELECTION_END_DATE)) and not request.user.is_superuser:
        return redirect('portal_home')

    tasks = Task.objects.filter(category=category).order_by('difficulty_value')
    submissions = Submission.objects.filter(user__user=request.user, task_submitted=True).values_list(
                'task_id', flat=True)
    # return render(request, 'portal/Tasks_2/index.html', {'category': category, 'tasks': tasks})
    return render(request, 'portal/categories/task.html', {'tasks': tasks, 'category': category, 'submissions': submissions})

@login_required(login_url='user_login')
def home(request):
    if Profile.objects.filter(user=request.user).exists():
        context = {
            'SELECTION_START_DATE' : SELECTION_START_DATE,
            'SELECTION_END_DATE' : SELECTION_END_DATE,
            'SELECTION_RESULT_DATE' : SELECTION_RESULT_DATE,
        }
        # return render(request, template_name='portal/taskcountdown.html', context=context)
        
        today = localtime(now())
        request.user.is_superuser = False
        
        if ((today < SELECTION_START_DATE) or (today > SELECTION_END_DATE)) and not request.user.is_superuser:
            name = 'task' if today < SELECTION_START_DATE else 'result'
            if today > SELECTION_RESULT_DATE:
                return redirect('selection_results')
            return render(request, template_name='portal/{}countdown.html'.format(name), context=context)
        else:

            categories = Category.objects.all().order_by('id')

            tasks = Task.objects.order_by('id')
            submissions = Submission.objects.filter(user__user=request.user).values_list(
                'task_id', flat=True)

            active_tasks = len(tasks)
            # return render(request, 'portal/Categories Screen/index.html', {'categories': categories})
            return render(request, 'portal/categories/index.html', {'categories': categories})

            return render(request, 'portal/main.html', {'tasks': tasks, 'active_tasks': active_tasks, 'submissions' : submissions, 'submission_deadline' : SELECTION_END_DATE})


            # return redirect('/library/')
        
    
    return redirect('user_signup')


@login_required(login_url='user_login')
def submit_task(request):
    today = localtime(now())
    if ((today < SELECTION_START_DATE) or (today > SELECTION_END_DATE)) and not request.user.is_superuser:
        return redirect('portal_home')
    
    if not request.POST.get('task_id', None) or not request.FILES.get('task_file', None):
        messages.error(request, "You forgot to select a file", extra_tags='danger')
        return redirect('portal_home')

    task_id = request.POST['task_id']
    file = request.FILES['task_file']
    
    user = request.user
    try:
        ace_profile_obj = Profile.objects.get(user=user)
        task_obj = Task.objects.get(pk=task_id)
    except ObjectDoesNotExist:
        messages.error(request, "Task does not exist", extra_tags='danger')
        return redirect('portal_home')

    submission_obj, created = Submission.objects.get_or_create(user=ace_profile_obj, task=task_obj)
    
    try:
        filename = "{}.{}-{} {}.{}".format(submission_obj.id, task_obj.task_name, task_obj.difficulty_value, now().strftime(DATETIME_FORMAT), file.name.rsplit('.', 1)[1].lower())
    except Exception:
        messages.error(request, "File must have extension", extra_tags="danger")
        return redirect('portal_home')
    #Save uploaded file to local storage
    tmp_storage_file = default_storage.save(os.path.join(MEDIA_ROOT, filename) , file)

    submission_obj.task_submitted = False
    submission_obj.submission_url = ''
    # if created:
    #     # task_obj.total_submissions = F('total_submissions') + 1
    #     task_obj.save()
    submission_obj.save()
    
    try:
        if not ace_profile_obj.submission_folder:
            ace_profile_obj.submission_folder = create_folder('{}#{}#{}'.format(ace_profile_obj.id, user.first_name, user.email), description="Submission folder of {}".format(user.email))
            ace_profile_obj.save()
    except Exception as e:
        print(e)
        print(str(e))
        print("error aa gya re")
        messages.error(request, "Could not upload your file", extra_tags='danger')
        return redirect('portal_home')

    t = threading.Thread(target=upload_drive_task, args=(filename, tmp_storage_file, submission_obj, ace_profile_obj.submission_folder))
    t.start()
    messages.success(request, 'Your task was submitted successfully') 
    return redirect('portal_home')


@login_required(login_url='user_login')
def serve_main_page(request):
    tasks = Task.objects.all().count()

    return render(request, 'portal/main.html',
                  {'fb_image_url': "image", 'first_name': "VIPS-ACE", 'tasks': tasks, 'active_tasks': tasks})


@login_required(login_url='user_login')
def selection_results(request):

    selected = SelectionResult.objects.all().select_related("user").distinct("user")

    profiles = []
    for row in selected:
        profiles.append(row.user)
    
    return render(request, 'portal/results.html', context={
        'profiles' : profiles
    })
# def error_404_view(request):
#     return render(request, 'portal/404.html') \

def refresh_token_view(request):
    try:
        refresh_token()
        return HttpResponse("OK", status=200)
    except Exception as e:
        return HttpResponse(str(e), status=400)


