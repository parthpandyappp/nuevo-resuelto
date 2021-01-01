from django.db import models

# Create your models here.


class resolute(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=20)
    author = models.CharField(max_length=20)
    body = models.TextField()
    done = models.BooleanField()
    created = models.DateField()
    modified = models.DateField()
    expires = models.DateField()

    def __str__(self):
        self.title
