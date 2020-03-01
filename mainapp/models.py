from django.db import models
from django.contrib.auth.models import User

# Create your models here.

NEW = 'NW'
IN_PROGRESS = 'INP'
IN_QA = 'INQ'
READY = 'RD'
DONE = 'DN'

STATUSES = [
    (NEW, 'New'),
    (IN_PROGRESS, 'In Progress'),
    (IN_QA, 'In QA'),
    (READY, 'Ready'),
    (DONE, 'Done'),
]

class Card(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()
    creator = models.ForeignKey(User, related_name='creator', on_delete=models.CASCADE)
    assignee = models.ForeignKey(User, related_name='assignee', on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    date_edited = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    status = models.CharField(max_length=12, choices=STATUSES, default=NEW)

    def __str__(self):
        return self.name