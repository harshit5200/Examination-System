from django.shortcuts import render, redirect
from .models import *
import json
import datetime
from django.contrib.auth import login, authenticate, logout
from .forms import SignUpForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse


ename=""
qcount=0
# Create your views here.

def showExamForm(request):
    if request.user.is_authenticated:
        return render(request, 'AddExam.html')


def addExam(request):
    if request.user.is_authenticated:
        global ename
        global qcount
        Ename = request.POST['exam-name']
        QuestionCount = request.POST['question-count']
        TotalMarks = request.POST['total-marks']
        Duration = request.POST['duration']
        StartDate = request.POST['startdate']
        StartTime = request.POST['starttime'] + ":00"
        EndTime = request.POST['endtime'] + ":00"
        E = Exams(Ename=Ename,QuestionCount=QuestionCount,Tmarks=TotalMarks,Duration=Duration,Date=StartDate,STime=StartTime,ETime = EndTime)
        ename = E
        qcount = QuestionCount
        E.save()
        return render(request, 'AddQuestion.html')

def addQuestion(request):
    if request.user.is_authenticated:
        global qcount
        qcount = int(qcount)
        while(qcount):
            Marks = request.POST['marks']
            Question =  request.POST['question']
            Option1 = request.POST['optA']
            Option2 = request.POST['optB']
            Option3 = request.POST['optC']
            Option4 = request.POST['optD']
            Answer = request.POST['correct']
            Q = Questions(Ename=ename,marks=Marks,Question=Question,option1=Option1,option2=Option2,option3=Option3,option4=Option4,Answer=Answer)
            Q.save()
            qcount = qcount - 1
            return render(request, 'AddQuestion.html')
        return render(request, 'AddExam.html')
   
def showStudent(request):
    Mark = None
    if request.user.is_authenticated:
        E = Exams.objects.all()
        M = Marks.objects.all()
        for i in M:
            if i.Name == request.user.username:
                if i.Ename.Date == datetime.date.today():
                    if str(i.Ename.STime) < datetime.datetime.now().strftime("%H:%M:%S") and str(i.Ename.ETime) > datetime.datetime.now().strftime("%H:%M:%S"):
                        if i.marks:
                            Mark = True
                        else:
                            Mark = False
        Ex = dict()
        for i in E:
            if i.Date == datetime.date.today():
                if str(i.STime) < datetime.datetime.now().strftime("%H:%M:%S") and str(i.ETime) > datetime.datetime.now().strftime("%H:%M:%S"):
                    Ex[i] = False
                else:
                    Ex[i] = True
        context = {'Exam':Ex, 'doneExam':Mark}
        return render(request, 'StudentPanel.html', context)

def startExam(request):
    if request.user.is_authenticated:
        questions = list()
        Q = Questions.objects.all()
        E = Exams.objects.all()
        t = None
        tmark = None
        stime=None
        etime=None
        for i in E:
            if str(i.STime) < datetime.datetime.now().strftime("%H:%M:%S") and str(i.ETime) > datetime.datetime.now().strftime("%H:%M:%S") and i.Date == datetime.date.today():
                t = i.Duration
                tmark = i.Tmarks
                stime = i.STime 
                etime = str(i.ETime)
        currenttime = datetime.datetime.now().strftime("%H:%M:%S")
        difftime = str(datetime.datetime.now().strptime(etime, "%H:%M:%S") - datetime.datetime.now().strptime(currenttime, "%H:%M:%S"))[2:4]
        ti = min(int(t), int(difftime))
        for i in Q:
            if str(i.Ename.STime) < datetime.datetime.now().strftime("%H:%M:%S") and str(i.Ename.ETime) > datetime.datetime.now().strftime("%H:%M:%S") and i.Ename.Date == datetime.date.today():
                l = [i.Question,i.option1,i.option2,i.option3,i.option4,i.Answer,i.marks]
                questions.append(l)
        question_list = json.dumps(questions)
        context = {'Time':ti, 'Question':question_list, 'Total':tmark}
        return render(request, 'ExamPanel.html',context)

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return render(request, 'AddExam.html')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                if request.user.username == 'minato':
                    return render(request, 'AddExam.html')
                else:
                    return redirect('/studentpanel')
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="login.html", context={"login_form":form})

def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.") 
    return render(request,'Logout.html')

def Result(request):
    username = request.user.username
    E = Exams.objects.all()
    en = None
    for i in E:
            if str(i.STime) < datetime.datetime.now().strftime("%H:%M:%S") and str(i.ETime) > datetime.datetime.now().strftime("%H:%M:%S") and i.Date == datetime.date.today():
                en = i
    res = request.POST['result']
    if not res:
        res = 0
    R = Marks(Name=username,Ename=en,marks=res)
    R.save()
    return redirect('/studentpanel')
    