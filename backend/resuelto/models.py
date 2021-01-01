from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class resolute(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=20)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    body = models.TextField()
    done = models.BooleanField()
    created = models.DateField()
    modified = models.DateField()
    expires = models.DateField()

    def __str__(self):
        return self.title
