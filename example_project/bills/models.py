import datetime
from django.db import models

class Bill(models.Model):
    company = models.CharField(max_length=150)
    amount = models.DecimalField(decimal_places=2, max_digits=7)
    due_date = models.DateTimeField(default=datetime.datetime.now)

    def __unicode__(self):
        return "Owe $%d to %s on %s" % (self.amount, self.company, self.due_date)
