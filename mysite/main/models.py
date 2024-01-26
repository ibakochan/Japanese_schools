from django.db import models
from accounts.models import CustomUser
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password



class Schedule(models.Model) :
    title = models.CharField(
            max_length=200,
    )


    CATEGORY_CHOICES = [
        ('Japanese_Basic_1', 'Japanese Basic 1'),
        ('Japanese_Basic_2', 'Japanese Basic 2'),
        ('Japanese_Basic_3', 'Japanese Basic 3'),
        ('Japanese_Basic_4', 'Japanese Basic 4'),
        ('Japanese_Advanced_1', 'Japanese Advanced 1'),
        ('Japanese_Advanced_2', 'Japanese Advanced 2'),
        ('Japanese_Advanced_3', 'Japanese Advanced 3'),
        ('Japanese_Advanced_4', 'Japanese Advanced 4'),
        ('Japanese_Expert_1', 'Japanese Expert 1'),
        ('Japanese_Expert_2', 'Japanese Expert 2'),
        ('Japanese_Expert_3', 'Japanese Expert 3'),
        ('Japanese_Expert_4', 'Japanese Expert 4'),
        ('Math', 'Math'),
        ('Science', 'Science'),
        ('Social_Studies', 'Social Studies'),
    ]




    # Color for the lesson title in the schedule.
    COLOR_CHOICES = [
        ('sky', 'Sky Blue'),
        ('green', 'Green'),
        ('yellow', 'Yellow'),
        ('purple', 'Purple'),
        ('pink', 'Pink'),
    ]


    color = models.CharField(max_length=20, choices=COLOR_CHOICES, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, null=True)
    picture = models.BinaryField(null=True, editable=True)
    content_type = models.CharField(max_length=256, null=True, help_text='The MIMEType of the file')


class Lesson(models.Model) :
    title = models.CharField(
            max_length=200,
    )

    # To decide which day in the schedule the lesson will be place in.
    DAY_CHOICES = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]


    # To decide in which order from top to bottom of the scheule the lesson will be placed.
    SPOT_CHOICES = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]


    # Color for the lesson title in the schedule.
    COLOR_CHOICES = [
        ('sky', 'Light Blue'),
        ('green', 'Green'),
        ('yellow', 'Yellow'),
        ('purple', 'Purple'),
        ('pink', 'Pink'),
    ]



    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    day = models.CharField(max_length=90, choices=DAY_CHOICES, null=True)
    spot = models.IntegerField(choices=SPOT_CHOICES, null=True)
    text = models.TextField(null=True)
    color = models.CharField(max_length=20, choices=COLOR_CHOICES, null=True)
    time = models.CharField(max_length=12, null=True)
    picture = models.BinaryField(null=True, editable=True)
    content_type = models.CharField(max_length=256, null=True, help_text='The MIMEType of the file')


class NameToDoLists(models.Model):
    name = models.CharField(max_length=200)
    password = models.CharField(max_length=200, blank=True, null=True)
    hashed_password = models.CharField(max_length=200, blank=True, null=True)

    def set_password(self, raw_password):
        self.hashed_password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.hashed_password)



class ToDoList(models.Model) :
    title = models.CharField(
            max_length=200,
    )

    name_to_do_lists = models.ForeignKey(NameToDoLists, on_delete=models.CASCADE, default=None)



class ParticipationCount(models.Model):
    # Taking monthly jiu jitsu participation counts and counts for each belt color.

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True)

    attendance = models.PositiveIntegerField(default=0)




class Click(models.Model):
    # For putting members names into the lesson to increase their participationcounts later.

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, default=None)
    timestamp = models.DateTimeField(auto_now_add=True)
    order = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.user)

class LateAbsence(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True)

    ABSENCE_CHOICES = [
        ('yes', 'Yes'),
    ]


    late = models.PositiveIntegerField(default=0)
    late_reason = models.TextField(null=True)
    absence = models.CharField(max_length=3, choices=ABSENCE_CHOICES, null=True)
    absence_reason = models.TextField(null=True)
    timestamp = models.DateTimeField(default=timezone.now)

class Grading(models.Model):

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)


    GRADING_CHOICES = [
        ('test', 'Test'),
        ('essay', 'Essay'),
        ('speech', 'Speech'),
    ]



    grading_picture = models.BinaryField(null=True, editable=True)
    grading_content_type = models.CharField(max_length=256, null=True, help_text='The MIMEType of the test picture')
    grading_material = models.CharField(max_length=10, choices=GRADING_CHOICES, blank=True, null=True)
    grading_material_grade = models.CharField(max_length=50, blank=True, null=True)
    grading_material_comment = models.TextField(blank=True, null=True)