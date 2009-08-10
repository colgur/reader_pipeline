from django.db import models

# Create your models here.
class User(models.Model):
   name = models.CharField(max_length=24)

   def __unicode__(self):
      return self.name

class Label(models.Model):
   user = models.ForeignKey(User)
   label = models.CharField(max_length=25)
   uri = models.CharField(max_length=50)
   frequency = models.IntegerField()

   def __unicode__(self):
      return self.label

class StopWord(models.Model):
   user = models.ForeignKey(User)
   stopword = models.CharField(max_length=25)

   def __unicode__(self):
      return self.stopword
