from django.db import models
from django.contrib.auth.models import User
from django.db.models import CASCADE


class ResolutionManager(models.Manager):
    def get_resolutions(self, **kwargs):
        """optionally takes a month, day, returns
        a limited queryset with up to 25 entries
        by default, or a single entry if given an id.
        """
        queryset = super().get_queryset()
        if kwargs.get('id', None):
            return queryset.get(id=kwargs['id'])

        if kwargs.get('month', None):
            queryset = queryset.filter(expires__month=kwargs['month'])

            if kwargs.get('day', None):
                queryset = queryset.filter(expires__day=kwargs['day'])

        return queryset

    def filter_resolutions(self, **kwargs):
        """takes offset, limit, and max_limit kwargs.
        If omitted will use default options.
        
        offset = resolution return offset
        limit = limit requested
        max_limit = maximum limit of return entries
        """
        queryset = super().get_queryset()
       
        offset = kwargs.get('offset', 0)
        if offset < 0:
            offset = 0

        max_limit = kwargs.get('max_limit', 25)
        if not isinstance(max_limit, int):
            max_limit = 25
        elif max_limit < 1:
            max_limit = 25

        limit = kwargs.get('limit', max_limit)
        if max_limit < limit or limit < 1:
            limit = max_limit

        limit = offset+limit
        queryset = queryset[offset:limit]
        
        return queryset

    def sort_resolutions(self, resolutions):
        """takes a list of resolutions and returns a sorted dictionary"""
        sorted_resolutions = {}
        for item in resolutions:
            if item.expires.month not in sorted_resolutions:
                sorted_resolutions[item.expires.month] = {}
            if item.expires.day not in sorted_resolutions[item.expires.month]:
                sorted_resolutions[item.expires.month][item.expires.day] = []
            sorted_resolutions[item.expires.month][item.expires.day].append(
                item)
        return sorted_resolutions


class resolute(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=20)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    body = models.TextField()
    done = models.BooleanField(default=False)
    created = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)
    expires = models.DateField()
    manager = ResolutionManager()

    '''def __str__(self):
        return {
            "title": self.title,
            "author": self.author,
            "done": self.done,
            "expires": self.expires,
            "body": self.body,
            "id": self.id
        }'''


class Bio(models.Model):
    id = models.AutoField(primary_key=True)
    body = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.body


class Joined(models.Model):
    joined_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resolution = models.ForeignKey(resolute, on_delete=models.CASCADE)
    # author = models.ForeignKey(User, on_delete=models.CASCADE)
