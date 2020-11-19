from datetime import date
from django.db import models


class PollQueryset(models.QuerySet):

    def active(self):
        today = date.today()
        return self.filter(starts__lte=today, ends__gte=today)
