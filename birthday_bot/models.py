from django.db import models
from django.contrib.auth.models import User
from pgvector.django import VectorField,IvfflatIndex
# Create your models here.



class Events(models.Model):
  
    date=models.DateField()
    event_en=models.TextField()
    event_bn=models.TextField()
    embedding=VectorField(dimensions=1536)


class UserQuery(models.Model):
    user= models.ForeignKey(User,on_delete=models.CASCADE)
    relation= models.CharField(max_length=200)
    question=models.TextField()
    answer=models.TextField(default=None)
    created_at=models.DateTimeField(auto_now_add=True)

    def __repr__(self):
        return f"Email:{self.user.email} [Question:{self.question}]" 



    

