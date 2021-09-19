import os
from os import path

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from ace.settings import BASE_DIR

API_KEY = "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"
sg = SendGridAPIClient(API_KEY)

with open(path.join(BASE_DIR, "Selection 2019 - result (1).tsv"), "r+") as f:
    tsv = f.read()

i = -1

for row in tsv.split("\n"):
    i = i + 1
    # if i < LAST_SENT or len(row) < 2:
    #     continue
    row = row.split("\t")

    name = row[0]
    email = row[6]
    message = Mail(
        from_email="noreply@vipsace.org",
        to_emails=email,
        subject="ACE Selections",
        html_content="""Dear {},<br>
<br>
We are pleased to inform you that you have been selected to join ACE 2019 as a {} member!<br>
<Br>
ACE Induction will be held on September 12, 2019 ,i.e., Thursday at 1 PM in room 306.<br>
<br>
We're looking forward to meet you.<br>
<br>

Congratulations and Welcome to the family! <br>
<br>
With love,<br>
Team ACE ❤.<br>
    """.format(
            name, "core" if row[1] == "Core" else ""
        ),
    )
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
