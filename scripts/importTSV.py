LAST_SENT = 0
from review.models import Review, SelectionResult, Profile
from django.db.models import Q
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


from ace.settings import BASE_DIR
from os import path
with open( path.join(BASE_DIR, 'Interview Review - Final List.tsv'), 'r+') as f:
    tsv = f.read()



data = []
i = -1

API_KEY = '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'

# tsv = '''0	Chirag Jain	Prog	BCA	1A	1:00	PM	Thursday'''

for row in tsv.split("\n"):
    i = i + 1
    if i < LAST_SENT or len(row) < 2:
        continue
    row = row.split("\t")

    print(row)

    name = row[0].split(" ")
    if len(name) == 2:
        qs = Profile.objects.filter(user__first_name=name[0], user__last_name=name[1])
    elif len(name) == 3:
        qs = Profile.objects.filter(Q(user__first_name="{} {}".format(name[0], name[1]), user__last_name=name[2]) | Q(user__first_name=name[0], user__last_name="{} {}".format(name[1], name[2])))
    else:
        qs = Profile.objects.filter(user__first_name=name[0])
    
    qs = qs.exclude(selectionresult=None)
    print( " ".join(name), qs.count() )
    if qs.count() > 1:
        raise Exception("More than 1 result")
    
    prof = qs[0]

    row.append(prof.email_id)
    row.append(prof.get_course_display())
    row.append(prof.get_section_display())
    row.append( str(prof.id) )

    data.append('\t'.join(row))

    
#     email = prof.email_id
#     date = '5' if str(row[6]).lower() == 'thursday' else '6'
#     sg = SendGridAPIClient( API_KEY )
#     message = Mail(from_email='noreply@vipsace.org',
#     to_emails=email,
#     subject='ACE Round 2',
#     html_content='''Hey {},<br>
# <br>
# Congratulations! <br>
# We are pleased to inform you that you have been shortlisted for the Interview round for ACE 2019, details for which are as follows :<br>
# <br>
# Date : <strong>{}th September 2019</strong><br>
# Time : <strong>{}</strong><br>
# Venue : <strong>Room 306, A-Block, VIPS</strong><br>
# <br>
# NOTE: <br>
# 1) Bring your laptops(fully charged) if you can<br>
# 2) Make sure you have the souce file for your submission<br>
# With Love,<br>
# Team ACE ❤<br>
# '''.format(prof.name(), date, row[5]))
#     response = sg.send(message)
#     print(response.status_code)
#     print(response.body)

with open( path.join(BASE_DIR, 'Selection 2019 - result (1).tsv'), 'w+') as f:
    f.write("\n".join(data))
