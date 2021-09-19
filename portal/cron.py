import os

from django_cron import CronJobBase, Schedule

from .drive import refresh_token


class RefreshToken(CronJobBase):
    RUN_EVERY_MINS = 50

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = "portal.refresh_token"

    def do(self):
        print(dict(os.environ))
        refresh_token()
