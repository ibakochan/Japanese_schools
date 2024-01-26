from django.contrib import admin
from main.models import Click, Lesson, ParticipationCount, Grading, LateAbsence, Schedule, NameToDoLists, ToDoList

admin.site.register([Click, Lesson, ParticipationCount, Grading, LateAbsence, Schedule, NameToDoLists, ToDoList])
