from django.contrib.auth.models import AbstractUser
from django.db import models
from multiselectfield import MultiSelectField
from datetime import datetime

class CustomUser(AbstractUser):

    # The categories are there to match the schedule categories in order to be able to place students in seperate schedules.
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


    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]


    date_of_birth = models.DateField(blank=True, null=True)

    @property
    def age(self):
        if self.date_of_birth:
            today = datetime.today()
            birth_date = self.date_of_birth
            age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            return age
        return None

    categories = MultiSelectField(choices=CATEGORY_CHOICES, default=[], max_length=255)
    date_of_birth = models.DateField(blank=True, null=True)
    # date_of_birth is currently not being used, but might be used later upon request.
    profile_picture = models.BinaryField(null=True, editable=True)
    content_type = models.CharField(max_length=256, null=True, help_text='The MIMEType of the file')
    # profile_picture and content_type are for upploading and streaming a picture for the user.
    # I got this from dj4e django tutorials assignments"
    user_limit = models.IntegerField(default=1000)
    nationality = models.CharField(max_length=50, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)










