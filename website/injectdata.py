from django.contrib.auth.models import User

from users.models import Profile

raise Exception("Cant call this")

members = """Anmol Jain,Y,,Akshey Arora
Devansh Taneja,Y,,Bhavika Arora
Kamal Nanda,,,Bhavishya Sahdev
Dhruv Maithil,Y,,Deepanshu Sarkar
Harshit Arora,,,Geetanjali
Kartik Vedi,,,Harshit Arora
Bhavika Arora,,,Kamal Nanda
Mehak Arora,Y,,Kartik Vedi
Yash Bindal,Y,,Mayank Anand
Pranav Bhatia,,Y,Mayank Mishra
Prateek Batra,Y,Y,Mridul Anand
Shreyans Jain,Y,Y,Raghav Tuli
Akshey Arora,,,Ritik Gupta
Akshita Jain,,Y,Riya Singh
Ansh Saini,Y,,Rohaan Mohammed
Mayank Mishra,,,Shubham Sehgal
Dikshant Rawat,Y,Y,Vaibhav Baweja
Gautam Chawla,Y,,Vasu Kataria
Geetansh Monga,,Y,Yash Upneja
Jay Tomar,Y,Y,
Jayesh Makkar,,Y,
Lakshay Kapoor,,Y,
Manik Gupta,Y,Y,
Mayank Anand,,,
Mohak Gupta,Y,Y,
Mridul Anand,,,
Naman Sharma,,Y,
Nikhil George,Y,,
Preetam Yadav,Y,,
Raghav Tuli,,,
Rohaan Mohammed,,,
Saransh Gupta,,Y,
Shubham Sehgal,,,
Tejus Sahi,,Y,
Vasu Kataria,,,
Yash Upneja,,,
Riya Singh,,,
Vaibhav Baweja,,,
Geetanjali ,,,
Ritik Gupta,,,
Agam Makhija,,,
Deepanshu Sarkar,,,
Bhavishya Sahdev,,,
Dhirendra Kumar Choudhary,Y,,
Chirag Jain,Y,Y,""".split(
    "\n"
)

for member in members:
    data = member.split(",")
    name = data[0]
    username = name.replace(" ", "").lower()
    user = User.objects.create_user(
        username=username,
        email=username + "@vipsace.org",
        password=None,
        first_name=name.split(" ")[0],
        last_name=name.split(" ")[1],
    )
    Profile.objects.create(
        is_member=True,
        is_core=(data[1] == "Y"),
        is_council=(data[2] == "Y"),
        user=user,
        email_id=username + "@vipsace.org",
        course=Profile.COURSE_BCA,
    )
