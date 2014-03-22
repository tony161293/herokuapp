from django.db import models
from django.contrib.auth.models import User


class Food_item(models.Model):

    def render(self, context):
        context[self.varname] = self.model._default_manager.all()[:self.num]
        return ''
    pub_date = models.DateField('date published')
    itemName = models.CharField(max_length=200, primary_key=True)
    cost = models.IntegerField()
    number = models.IntegerField()

    def __unicode__(self):
        return '%s' % (self.itemName)

    def save(self, *args, **kwargs):
            Food_item.objects.all().order_by('-pub_date')
            super(Food_item, self).save(*args, **kwargs)


class UserProfile(models.Model):

    # This line is required. Links UserProfile to a User model instance.

    user = models.OneToOneField(User)
    Admn_no = models.CharField(max_length=10, primary_key=True)
    Credit = models.IntegerField(default=0)
    Name = models.CharField(max_length=40)
    Batch = models.IntegerField()

    def __unicode__(self):
        return '%s' % (self.Name)


class orderDetails(models.Model):

    useradno = models.CharField(max_length=10)
    itemname = models.CharField(max_length=200)
    order_date = models.DateField('date ordered')
    count = models.IntegerField()

    def __unicode__(self):
        return str(self.useradno)