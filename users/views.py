from .models import Profile
from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# Create your views here.

SECTIONS = [x for x,y in Profile.SECTIONS]
COURSES = [x for x,y in Profile.COURSES]

def login(request):
    if request.user.is_authenticated:
        if not Profile.objects.filter(user=request.user).exists():
            return redirect('user_signup')
        else:
            # return redirect('home')
            return redirect('index')

    return render(request, 'users/login.html')

    
def logout(request):
    auth_logout(request)
    return redirect('index')


@login_required(login_url='user_login')
def signup(request):
    if not Profile.objects.filter(user=request.user).exists():
        
        if request.method == 'POST':
            user = request.user
            # if Profile.objects.filter(user=user).exists():
            #     return redirect('portal_home')

            phone = str(request.POST.get('phone', '')).strip()[-10:]
            enrollment_number = request.POST.get('enrollment_number', None)
            course = int(request.POST.get('course', 0))
            email_id = request.POST.get('email', None)
            section = int(request.POST.get('section', 0))
            first_name = request.POST.get('first_name', None)
            last_name = request.POST.get('last_name', None)
            dob = request.POST.get('dob', None)

            errors = {}
            if len(phone) < 10:
                errors['phone'] = 'Contact Number must be atleast 10 characters long'
            elif len(phone) > 11:
                errors['phone'] = 'Contact Number can\'t be more than 10 characters long'
            elif not phone.isdigit():
                errors['phone'] = 'Contact Number can contain only digits'
            elif Profile.objects.filter(phone_number=phone).exists():
                errors['phone'] = 'Contact Number already registered'

            if not email_id:
                errors['email'] = 'Email Address is required'
            elif Profile.objects.filter(email_id=email_id).exists():
                errors['email'] = 'Email Address already registered'

            if course not in COURSES:
                errors['course'] = 'Invalid Course Selected'
            
            if section not in SECTIONS:
                errors['section'] = 'Invalid Section Selected'

            if not first_name or len(first_name) < 3:
                errors['first_name'] = 'First Name must be atleast 3 characters long'

            if last_name and len(str(last_name)) < 2:
                errors['last_name'] = 'Last Name must be atleast 3 characters long'
            
            if not dob:
                errors['dob'] = 'Date Of Birth is required'
            # else:

            if enrollment_number is not None and len(str(enrollment_number)) > 0:
                if len(str(enrollment_number)) != 11:
                    errors['enrollment_number'] = 'Enrollment number must be exactly 11 digits long'
                elif not str(enrollment_number).isdigit():
                    errors['enrollment_number'] = 'Enrollment number can only contain digits'
            
            if bool(errors):
                return render(request, 'users/signup.html', context={
                    'errors' : errors
                })

            user.first_name = first_name
            user.last_name = last_name
            user.save()

            try:
                ace_user = Profile.objects.create(user=user, enrollment_number=enrollment_number, course=course, email_id=email_id,
                                    section=section, phone_number=phone)
            except Exception as e:
                print(str(e))
                return render(request, 'users/signup.html', context={'errors': {}})
            # ace_user.save()

            return redirect('portal_home')
        else:
            return render(request, 'users/signup.html', context={'errors': {}})

    return redirect('portal_home')