from django import forms
from main.models import Schedule, Lesson, ParticipationCount, LateAbsence, Grading, NameToDoLists, ToDoList
from django.core.files.uploadedfile import InMemoryUploadedFile
from accounts.models import CustomUser
from main.humanize import naturalsize
from django.forms import DateInput
from django.core.exceptions import ValidationError





class UserPreferencesForm(forms.ModelForm):
    # This form lets you upload a profile picture and select belt, stripes, member type, gym, for a member.
    # everything about uploading pictures I got from the dj4e tutorial.
    max_upload_limit = 2 * 1024 * 1024
    max_upload_limit_text = naturalsize(max_upload_limit)

    # for uploading a picture max 2mb large.
    profile_picture = forms.FileField(required=False, label='max size <= '+max_upload_limit_text)
    upload_field_name = 'profile_picture'

    date_of_birth = forms.DateField(
        label='Date of birth',
        widget=DateInput(attrs={'type': 'date'}),
        required=False
    )


    # using widgets to get it looking a little bit nicer.
    class Meta:
        model = CustomUser
        fields = ['categories', 'profile_picture', 'date_of_birth', 'nationality', 'gender']

        widgets = {
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'nationality': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
        }



    def clean(self):
        # Enforces the upload limit and gives an error text when the file is above the limit which is 2mb.
        cleaned_data = super().clean()
        user = cleaned_data.get('profile_picture')
        if user is None:
            return
        if len(user) > self.max_upload_limit:
            self.add_error('profile_picture', "Max size < "+self.max_upload_limit_text+" bytes")

    def save(self, commit=True):
        instance = super(UserPreferencesForm, self).save(commit=False)

        # Creating an instance from the form to save it in the model.
        f = instance.profile_picture
        if isinstance(f, InMemoryUploadedFile):
            bytearr = f.read()
            instance.content_type = f.content_type
            instance.profile_picture = bytearr

        if commit:
            instance.save()

        return instance


class GradingMaterialForm(forms.ModelForm):
    # This form lets you record graded material.

    max_upload_limit = 2 * 1024 * 1024
    max_upload_limit_text = naturalsize(max_upload_limit)

    # for uploading a picture max 2mb large.
    grading_picture = forms.FileField(required=False, label='Max size <= '+max_upload_limit_text)
    upload_field_name = 'grading_picture'


    # using widgets to get it looking a little bit nicer.
    class Meta:
        model = Grading
        fields = ['grading_material', 'grading_material_grade', 'grading_material_comment', 'grading_picture']

        widgets = {
            'grading_material': forms.Select(attrs={'class': 'form-control'}),
            'grading_material_grade': forms.TextInput(attrs={'label': 'Grading Material Grade'}),
            'grading_material_comment': forms.Textarea(attrs={'label': 'Grading Material Comment', 'style': 'height: 100px; vertical-align: top;'}),
        }



    def clean(self):
        # Enforces the upload limit and gives an error text when the file is above the limit which is 2mb.
        cleaned_data = super().clean()
        user = cleaned_data.get('grading_picture')
        if user is None:
            return
        if len(user) > self.max_upload_limit:
            self.add_error('grading_picture', "File must be < "+self.max_upload_limit_text+" bytes")

    def save(self, commit=True):
        instance = super(GradingMaterialForm, self).save(commit=False)

        f = instance.grading_picture
        if isinstance(f, InMemoryUploadedFile):
            bytearr = f.read()
            instance.grading_content_type = f.content_type
            instance.grading_picture = bytearr

        if commit:
            instance.save()

        return instance






class ParticipationCountForm(forms.ModelForm):
    # This form lets you update a member participation count manually
    # This is so that the teachers of the school can manually add previous attendance counts that were in paper form.
    class Meta:
        model = ParticipationCount
        fields = ['attendance']

        #Using widgets again for some style.
        widgets = {
            'attendance': forms.TextInput(attrs={'class': 'form-control col-2'}),
        }





class CreateForm(forms.ModelForm):
    # This is a form for creating a lesson in the schedule.
    # You can write a title, time, upload a picture, choose day, spot in the schedule and color.
    max_upload_limit = 2 * 1024 * 1024
    max_upload_limit_text = naturalsize(max_upload_limit)

    picture = forms.FileField(required=False, label='Max size <= '+max_upload_limit_text)
    upload_field_name = 'picture'


    days = forms.MultipleChoiceField(
        choices=Lesson.DAY_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        label='Day'
    )

    class Meta:
        model = Lesson
        fields = ['title', 'spot', 'time', 'color', 'picture', 'days']



        #Using widgets again for some style.
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'spot': forms.Select(attrs={'class': 'form-control'}),
            'time': forms.TextInput(attrs={'class': 'form-control'}),
            'color': forms.Select(attrs={'class': 'form-control'}),
        }



    def clean(self):
        cleaned_data = super().clean()
        lesson = cleaned_data.get('picture')


        if lesson is None:
            raise ValidationError("Please upload a picture.")
        if len(lesson) > self.max_upload_limit:
            self.add_error('picture', "File must be < "+self.max_upload_limit_text+" bytes")


    def save(self, commit=True):
        instance = super(CreateForm, self).save(commit=False)

        f = instance.picture
        if isinstance(f, InMemoryUploadedFile):
            bytearr = f.read()
            instance.content_type = f.content_type
            instance.picture = bytearr

        if commit:
            instance.save()

        return instance






class LateAbsenceForm(forms.ModelForm):
    # Form for recording late/absence.

    class Meta:
        model = LateAbsence
        fields = ['late', 'late_reason', 'absence', 'absence_reason']

        # Using widgets again for some style.
        widgets = {
            'late': forms.NumberInput(attrs={'class': 'form-control'}),
            'late_reason': forms.TextInput(attrs={'class': 'form-control'}),
            'absence': forms.Select(attrs={'class': 'form-control'}),
            'absence_reason': forms.TextInput(attrs={'class': 'form-control'}),
        }



    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].required = False



class ScheduleCreateForm(forms.ModelForm):
    # This is a form for creating a schedule.
    # You can write a title, choose color, category and upload a picture.
    max_upload_limit = 2 * 1024 * 1024
    max_upload_limit_text = naturalsize(max_upload_limit)

    picture = forms.FileField(required=False, label='Upload limit <= '+max_upload_limit_text)
    upload_field_name = 'picture'



    class Meta:
        model = Schedule
        fields = ['title', 'color', 'category', 'picture']

        #Using widgets again for some style.
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'color': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        lesson = cleaned_data.get('picture')
        if lesson is None:
            return
        if len(lesson) > self.max_upload_limit:
            self.add_error('picture', "File must be < "+self.max_upload_limit_text+" bytes")



    def save(self, commit=True):
        instance = super(ScheduleCreateForm, self).save(commit=False)

        f = instance.picture
        if isinstance(f, InMemoryUploadedFile):
            bytearr = f.read()
            instance.content_type = f.content_type
            instance.picture = bytearr

        if commit:
            instance.save()

        return instance


class NameToDoListsForm(forms.ModelForm):
    # Form for making a ToDoList.

    class Meta:
        model = NameToDoLists
        fields = ['name', 'password']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }


class ToDoListForm(forms.ModelForm):
    # Form for writing down things to do in your ToDoList.

    class Meta:
        model = ToDoList
        fields = ['title']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'title': 'Todo',
        }

