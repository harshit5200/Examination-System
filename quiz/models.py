from django.db import models

# Create your models here.
class Students(models.Model):
    Name = models.CharField(max_length=30)
    Password = models.CharField(max_length=20)
    Email = models.EmailField()
    Contact = models.CharField(max_length=10)

class Questions(models.Model):
    Qid = models.AutoField(primary_key=True)
    Ename = models.ForeignKey('Exams', on_delete=models.CASCADE)
    marks = models.PositiveIntegerField(default=0)
    Question = models.TextField(max_length=500)
    option1 = models.CharField(max_length=20)
    option2 = models.CharField(max_length=20)
    option3 = models.CharField(max_length=20)
    option4 = models.CharField(max_length=20)
    Answer = models.CharField(max_length=1)

class Exams(models.Model):
    Ename = models.CharField(max_length=50)
    Date = models.DateField()
    STime = models.TimeField()
    ETime = models.TimeField()
    QuestionCount = models.CharField(max_length=20)
    Tmarks = models.CharField(max_length=20)
    Duration = models.CharField(max_length=5)

class Result(models.Model):
    Name = models.ForeignKey('Students', on_delete=models.CASCADE)
    Ename = models.ForeignKey('Exams', on_delete=models.CASCADE)
    marks = models.CharField(max_length=3)
