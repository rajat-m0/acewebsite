from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout

from website.models import Achievement, Event, Gallery, Archive
from users.models import Profile, Mentor, Alumni
# from website.projectsjson import projects

def index(request):
    events = Event.objects.all()[:3]
    members = Profile.objects.filter(is_council=True).order_by('rank')
    calendar = []

    print(f"Profile Countr: {members}")

    from .projectsjson import projects
    
    return render(request, template_name='website/index.html',
                  context={'members': members, 'events': events, 'calendar': calendar, 'projects': projects[:3]})


def member(request):
    members = Profile.objects.filter(is_member=True)

    print(f"Profile Counter: {Profile.objects.count()}")

    return render(request, template_name='website/member.html', context={'members': members})


def mentor(request):
    mentors = Mentor.objects.all().order_by('id')
    return render(request, template_name='website/mentor.html', context={'mentors': mentors})


def alumni(request):
    alumnus = Alumni.objects.all()
    return render(request, template_name='website/alumni.html', context={'alumnus': alumnus})


def event(request):
    events = Event.objects.all()
    return render(request, template_name='website/events.html', context={'events': events})


def project(request):
    #projects = Project.objects.all()
    from .projectsjson import projects
    
    return render(request, template_name='website/projects.html', context={'projects': projects})


def achievement(request):
    achievements = Achievement.objects.all()
    return render(request, template_name='website/achievement.html', context={'achievements': achievements})

def archive(request):
    archive = Archive.objects.all()
    return render(request, template_name='website/archive.html', context={'archive': archive})

def agenda(request):
    # agendas = Agenda.objects.all()
    agendas = []
    return render(request, template_name='website/calendar.html', context={'agendas': agendas})


def codeofconduct(request):
    return render(request, template_name='website/codeofconduct.html')


def selection(request):
    return render(request, template_name='website/selection.html')


# other stuff

def magazine2017(request):
    return redirect('https://bit.ly/ACEMag2017')

def magazine2018(request):
    return redirect('https://bit.ly/ACEMag2018')

def magazine2019(request):
    return redirect('https://bit.ly/ACEMag2019')

def magazine2020(request):
    return redirect('https://bit.ly/acemagv4')

def magazine2021(request):
    return redirect('https://bit.ly/ACEMag2021')



def view_404(request, exception):
    return redirect('/')


def logout(request):
    auth_logout(request)
    return redirect('/library/')
