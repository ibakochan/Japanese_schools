from django.shortcuts import render, redirect
from django.views import View
from main.models import Click, Schedule, Lesson, ParticipationCount, LateAbsence, Grading, NameToDoLists, ToDoList
from django.urls import reverse
from django.shortcuts import HttpResponseRedirect
from accounts.models import CustomUser
from django.http import JsonResponse
from django.utils import timezone
from django.core import serializers
from django import forms
from accounts.forms import CustomUserCreationForm
from django.contrib import messages








from main.forms import CreateForm, ScheduleCreateForm, UserPreferencesForm, ParticipationCountForm, LateAbsenceForm, GradingMaterialForm, NameToDoListsForm, ToDoListForm
from django.contrib.auth.mixins import LoginRequiredMixin
from main.owner import OwnerDeleteView
from django.shortcuts import get_object_or_404
from django.http import HttpResponse





class SetUserLimitView(View):
    # For setting a limit to the number of members allowed.
    # This is being used with a middle ware that prevents access to the signup page if the limit is reached.
    template_name = 'main/profile.html'

    def post(self, request, *args, **kwargs):
        user_limit = request.POST.get('user_limit')
        current_user = self.request.user
        current_user.user_limit = int(user_limit)
        current_user.save()
        return redirect('main:profile', user_id=current_user.id)




class ProfilePageView(LoginRequiredMixin, View):
    # View for displaying details of a member.
    # Includes various things like profile pic, belt color, participation counts etc.

    model = CustomUser
    template_name = 'main/profile.html'




    def get(self, request, user_id):
        # Gets the current belt, gym etc for the UserPreferencesForm.
        # And gets the current participation counts for the user as initial input in the form.
        user = get_object_or_404(CustomUser, id=user_id)
        users = CustomUser.objects.all()
        grading = Grading.objects.filter(user=user)
        late_absence = LateAbsence.objects.filter(user=user)
        participation_counts = ParticipationCount.objects.filter(user=user)
        total_attendance = sum(pc.attendance for pc in participation_counts)


        CATEGORY_CHOICES = CustomUser.CATEGORY_CHOICES
        categories = [choice[0] for choice in CATEGORY_CHOICES]
        japanese_categories = [choice[1] for choice in CATEGORY_CHOICES]
        zipped_data = zip(categories, japanese_categories)

        user_preferences_form = UserPreferencesForm(instance=user)
        grading_form = GradingMaterialForm(instance=user)
        participation_count_form = ParticipationCountForm(initial={'attendance': total_attendance,})
        signup_form = CustomUserCreationForm()
        late_absence_form = LateAbsenceForm(initial={'user': user.pk})



        return render(request, self.template_name, {
            'zipped_data': zipped_data,
            'japanese_categories': japanese_categories,
            'categories': categories,
            'user': user,
            'users': users,
            'user_preferences_form': user_preferences_form,
            'participation_count_form': participation_count_form,
            'signup_form': signup_form,
            'late_absence_form': late_absence_form,
            'grading': grading,
            'late_absence': late_absence,
            'grading_form': grading_form,
            'total_attendance': total_attendance,
        })

    def get_context_data(self, **kwargs):
        # To get the user of the current profile page.
        context = super(ProfilePageView, self).get_context_data(**kwargs)
        user_id = self.kwargs['user_id']

        user_id = int(user_id)

        context['user_id'] = user_id
        return context

    def post(self, request, user_id):
        # For changing information about the user using the form.

        user = get_object_or_404(CustomUser, id=user_id)

        user_preferences_form = UserPreferencesForm(request.POST, request.FILES or None, instance=user)
        late_absence_form = LateAbsenceForm(request.POST)
        grading_form = GradingMaterialForm(request.POST, request.FILES or None)
        signup_form = CustomUserCreationForm(request.POST)


        if signup_form.is_valid():
            user = signup_form.save()
            return redirect('main:profile', user_id=user.id)
        else:
            messages.error(request, 'Username or Password are invalid. Please try again.')


        if grading_form.is_valid():
            grading = grading_form.save(commit=False)
            grading.owner = self.request.user
            grading.user = user
            grading.save()

        if user_preferences_form.is_valid():
            user_preferences_form.save()

        if late_absence_form.is_valid():
            late_absence = late_absence_form.save(commit=False)
            late_absence.user = user
            late_absence.save()

        return redirect('main:profile', user_id=user.id)






def profile_stream_file(request, user_id):
    # This is got from the dj4e tutorial.
    # Lets you stream the picture in a different url and so I can use that link to display it on a page.

    user = get_object_or_404(CustomUser, id=user_id)
    response = HttpResponse()
    response['Content-Type'] = user.content_type
    response['Content-Length'] = len(user.profile_picture)
    response.write(user.profile_picture)
    return response





class ParticipationCountView(View):
    # Lets you change the participation count of a user manually using the form.

    template_name = 'main/profile.html'

    def post(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)

        ParticipationCount.objects.filter(user=user).delete()
        participation_count = ParticipationCount.objects.create(user=user)

        form = ParticipationCountForm(request.POST, instance=participation_count)

        if form.is_valid():


            participation_count.save()

            success_url = reverse('main:profile', kwargs={'user_id': participation_count.user.id})
            return redirect(success_url)
        else:
            return render(request, self.template_name, {'user': user, 'form': form, 'participation_count': participation_count})




class ProfileParticipationIncreaseView(LoginRequiredMixin, View):
    # Lets you increase a members participation count for monthly count and its current belt color.
    # I made it a jsonresponse to use ajax to not refresh the page after each increase.
    # I added serialize and timestamp to be able to order member from most recent participants.

    def post(self, request, user_id):
        user = CustomUser.objects.get(pk=user_id)



        participation_count, created = ParticipationCount.objects.get_or_create(user=user, lesson=None)

        participation_count.attendance += 1


        participation_count.save()


        response_data = {
            'user_id': user.id,
            'updated_counts': {
                'attendance':  participation_count.attendance,
            },
        }

        return JsonResponse(response_data)



class AccountDeleteView(OwnerDeleteView):
    # Using the OwnerDeleteView I got from dj4e to delete accounts.

    model = CustomUser
    template_name = 'main/profile.html'

    def get_success_url(self):
        current_user_id = self.request.user.id
        return reverse('main:profile', kwargs={'user_id': current_user_id})










class GradingView(LoginRequiredMixin, View):

    template_name = 'main/grading.html'

    def get(self, request, pk):
        user = get_object_or_404(CustomUser, pk=pk)
        form = GradingMaterialForm(instance=user)
        ctx = {'form': form, 'user': user}
        return render(request, self.template_name, ctx)

    def post(self, request, pk):
        user = get_object_or_404(CustomUser, pk=pk)
        form = GradingMaterialForm(request.POST, request.FILES or None)

        if form.is_valid():
                grading = form.save(commit=False)
                grading.owner = self.request.user
                grading.user = user
                grading.save()
                return redirect('main:profile', user_id=user.id)




def grading_stream_file(request, pk):
    # same kind of picture stream as the one used for profile pics.

    grading_material = get_object_or_404(Grading, id=pk)
    response = HttpResponse()
    response['Content-Type'] = grading_material.grading_content_type
    response['Content-Length'] = len(grading_material.grading_picture)
    response.write(grading_material.grading_picture)
    return response









class ScheduleCreateView(LoginRequiredMixin, View):
    # View for creating a lesson using the Createform.

    template_name = 'main/schedule_form.html'

    def get(self, request, pk=None):
        form = ScheduleCreateForm()
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        form = ScheduleCreateForm(request.POST, request.FILES or None)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        if form.is_valid():
                schedule = form.save(commit=False)
                schedule.owner = self.request.user
                schedule.save()
                return redirect('main:schedules')

        else:
            ctx = {'form': form}
            return render(request, self.template_name, ctx)




class ScheduleUpdateView(LoginRequiredMixin, View):

    template_name = 'main/schedule_update.html'

    def get(self, request, pk):
        schedule = Schedule.objects.get(pk=pk)
        form = ScheduleCreateForm(instance=schedule)
        ctx = {'form': form, 'schedule': schedule}
        return render(request, self.template_name, ctx)

    def post(self, request, pk):
        schedule = Schedule.objects.get(pk=pk)
        form = ScheduleCreateForm(request.POST, request.FILES or None, instance=schedule)

        if not form.is_valid():
            ctx = {'form': form, 'schedule': schedule}
            return render(request, self.template_name, ctx)

        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.owner = self.request.user
            schedule.save()
            return redirect('main:schedules')
        else:
            ctx = {'form': form, 'schedule': schedule}
            return render(request, self.template_name, ctx)




class ScheduleListView(LoginRequiredMixin, View):
    # For displaying Iwade lessons on the page.

    model = Schedule
    template_name = "main/schedules.html"

    def get(self, request) :
        schedules = Schedule.objects.all()

        ctx = {
            'schedules' : schedules,
        }
        return render(request, self.template_name, ctx)




class ScheduleView(LoginRequiredMixin, View):
    template_name = 'main/schedule.html'

    def get(self, request, pk):
        schedule = get_object_or_404(Schedule, pk=pk)
        lessons = Lesson.objects.filter(schedule=schedule)
        day_choices = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        spots = range(1, 6)


        ctx = {
            'schedule': schedule,
            'lessons': lessons,
            'day_choices': day_choices,
            'spots': spots,
            }
        return render(request, self.template_name, ctx)




class ScheduleDeleteView(OwnerDeleteView):
    # Lets you delete a lesson.
    # Deleting a lesson does not affect any participation counts associated with the lesson.
    model = Schedule

    def get_success_url(self):
        return reverse('main:schedules')






def schedule_stream_file(request, pk):
    # same kind of picture stream as the one used for profile pics.

    schedule = get_object_or_404(Schedule, id=pk)
    response = HttpResponse()
    response['Content-Type'] = schedule.content_type
    response['Content-Length'] = len(schedule.picture)
    response.write(schedule.picture)
    return response










class NewLessonCreateView(LoginRequiredMixin, View):
    # View for creating a lesson using the Createform.

    template_name = 'main/new_lesson_form.html'

    def get(self, request, pk):
        schedule = get_object_or_404(Schedule, pk=pk)
        form = CreateForm(initial={'schedule': schedule})
        ctx = {'form': form, 'schedule': schedule}
        return render(request, self.template_name, ctx)

    def post(self, request, pk):
        schedule = get_object_or_404(Schedule, pk=pk)
        form = CreateForm(request.POST, request.FILES or None)

        if not form.is_valid():
            ctx = {'form': form, 'schedule': schedule}
            return render(request, self.template_name, ctx)

        selected_days = form.cleaned_data['days']

        for day in selected_days:
            lesson_spot_used = Lesson.objects.filter(day=day, spot=form.cleaned_data['spot'], schedule=schedule).exists()

            if not lesson_spot_used:
                form.cleaned_data['picture'].seek(0)
                picture_data = form.cleaned_data['picture'].read()
                Lesson.objects.create(
                    schedule=schedule,
                    day=day,
                    title=form.cleaned_data['title'],
                    spot=form.cleaned_data['spot'],
                    time=form.cleaned_data['time'],
                    color=form.cleaned_data['color'],
                    picture=picture_data,
                    )

            else:
                ctx = {'form': form, 'error_message': 'This day and spot already exist.', 'schedule': schedule}
                return render(request, self.template_name, ctx)

        return redirect('main:schedule', pk=schedule.pk)






class LessonUpdateView(LoginRequiredMixin, View):

    template_name = 'main/lesson_update.html'

    def get(self, request, pk):
        lesson = Lesson.objects.get(pk=pk)
        initial_data = {
            'title': lesson.title,
            'spot': lesson.spot,
            'time': lesson.time,
            'color': lesson.color,
            'days': lesson.day,
        }
        form = CreateForm(instance=lesson, initial=initial_data)
        form.fields['days'].widget = forms.Select(choices=Lesson.DAY_CHOICES)
        ctx = {'form': form, 'lesson': lesson}
        return render(request, self.template_name, ctx)

    def post(self, request, pk):
        lesson = Lesson.objects.get(pk=pk)
        form = CreateForm(request.POST, request.FILES or None, instance=lesson)

        if not form.is_valid():
            ctx = {'form': form, 'lesson': lesson}
            return render(request, self.template_name, ctx)

        if form.is_valid():
            schedule = lesson.schedule
            days = form.cleaned_data['days']
            spot = form.cleaned_data['spot']

            # Iterate through the list of days
            for day in days:
                lesson_spot_used = Lesson.objects.filter(day=day, spot=spot, schedule=schedule).exclude(pk=pk).exists()

                if not lesson_spot_used:
                    lesson = form.save(commit=False)
                    lesson.owner = self.request.user
                    lesson.schedule = schedule
                    lesson.day = day  # Set the individual day
                    lesson.save()
                else:
                    ctx = {'form': form, 'lesson': lesson, 'error_message': 'This day and spot already exist.'}
                    return render(request, self.template_name, ctx)

            return redirect('main:schedule', pk=schedule.pk)
        else:
            ctx = {'form': form, 'lesson': lesson}
            return render(request, self.template_name, ctx)




class LessonView(LoginRequiredMixin, View):
    # Lets you add a member to a lesson.

    template_name = 'main/lesson.html'
    model = Click

    def get(self, request, pk):

        lesson = Lesson.objects.get(pk=pk)
        clicks = Click.objects.filter(lesson=lesson)
        ctx = {
            'clicks': clicks,
            'lesson': lesson,
        }
        return render(request, self.template_name, ctx)

    def post(self, request, pk):
        lesson = Lesson.objects.get(pk=pk)
        click = Click.objects.get(lesson=lesson)
        user = click.user

        participation_count, created = ParticipationCount.objects.get_or_create(
            user=user,
            lesson=lesson
        )

        participation_count.attendance += 1


        participation_count.save()

        click.order = timezone.now()
        click.timestamp = timezone.now()
        click.save()

        clicks = Click.objects.filter(lesson=lesson, user=user).order_by('-order')

        clicks_json = serializers.serialize('json', clicks)


        response_data = {
            'user_id': user.id,
            'click_id': click.id,
            'timestamp': click.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            'updated_counts': {
                'attendance':  participation_count.attendance,
            },
            'clicks': clicks_json,
        }

        return JsonResponse(response_data)



class AddUsersToLessonsView(View):
    # Lets you add each member to all lessons of each respective school.

    template_name = 'main/bjj_lesson_list.html'

    def post(self, request, *args, **kwargs):
        # Get all users and lessons
        all_users = CustomUser.objects.all()
        all_lessons = Lesson.objects.all()

        # Iterate through each user and each lesson to create or delete Clicks
        for user in all_users:
            for lesson in all_lessons:
                # Check if the user's categories match the lesson's schedule category
                if lesson.schedule and user.categories and lesson.schedule.category in user.categories:
                    # Create or update Click
                    Click.objects.get_or_create(user=user, lesson=lesson)
                else:
                    # Delete Click if it exists
                    Click.objects.filter(user=user, lesson=lesson).delete()

        return HttpResponseRedirect(reverse('main:schedules'))





class LateAbsenceFormView(LoginRequiredMixin, View):
    template_name = 'main/late_absence_form.html'

    def get(self, request, pk):
        user = get_object_or_404(CustomUser, pk=pk)
        late_absence = LateAbsence.objects.filter(user=user)

        # Prepopulate the form with the user data
        form = LateAbsenceForm(initial={'user': user.pk})

        ctx = {'form': form, 'late_absence': late_absence, 'user': user}
        return render(request, self.template_name, ctx)

    def post(self, request, pk):
        user = get_object_or_404(CustomUser, pk=pk)
        form = LateAbsenceForm(request.POST)

        if form.is_valid():

            late_absence = form.save(commit=False)
            late_absence.user = user

            late_absence.save()
            # Redirect to the LessonView with the lesson's primary key
            return redirect('main:profile', user_id=user.pk)
        else:
            ctx = {'form': form, 'user': user}
            return render(request, self.template_name, ctx)



class LateAbsenceView(LoginRequiredMixin, View):
    # Lets you add a member to a lesson.

    template_name = 'main/late_absence.html'
    model = LateAbsence

    def get(self, request, pk):

        user = get_object_or_404(CustomUser, pk=pk)
        late_absence = LateAbsence.objects.filter(user=user)
        ctx = {
            'late_absence': late_absence, 'user': user
        }
        return render(request, self.template_name, ctx)





class ParticipationIncreaseView(LoginRequiredMixin, View):
    # Lets you increase a members participation count for monthly count and its current belt color.
    # I made it a jsonresponse to use ajax to not refresh the page after each increase.
    # I added serialize and timestamp to be able to order member from most recent participants.

    def post(self, request, pk, click_id):
        lesson = Lesson.objects.get(pk=pk)
        click = Click.objects.get(pk=click_id, lesson=lesson)
        user = click.user

        participation_count, created = ParticipationCount.objects.get_or_create(
            user=user,
            lesson=lesson
        )

        participation_count.attendance += 1


        participation_count.save()

        click.order = timezone.now()
        click.timestamp = timezone.now()
        click.save()

        clicks = Click.objects.filter(lesson=lesson, user=user).order_by('-order')

        clicks_json = serializers.serialize('json', clicks)


        response_data = {
            'user_id': user.id,
            'click_id': click.id,
            'timestamp': click.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            'updated_counts': {
                'attendance':  participation_count.attendance,
            },
            'clicks': clicks_json,
        }

        return JsonResponse(response_data)



class LessonDeleteView(OwnerDeleteView):
    # Lets you delete a lesson.
    # Deleting a lesson does not affect any participation counts associated with the lesson.

    model = Lesson

    def get_success_url(self):
        lesson = self.get_object()
        schedule = lesson.schedule

        return reverse('main:schedule', kwargs={'pk': schedule.pk})



def stream_file(request, pk):
    # same kind of picture stream as the one used for profile pics.

    lesson = get_object_or_404(Lesson, id=pk)
    response = HttpResponse()
    response['Content-Type'] = lesson.content_type
    response['Content-Length'] = len(lesson.picture)
    response.write(lesson.picture)
    return response









class NameToDoListsCreateView(LoginRequiredMixin, View):
    # View for creating a lesson using the Createform.

    template_name = 'main/name_to_do_lists_form.html'

    def get(self, request):
        form = NameToDoListsForm()
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request):
        form = NameToDoListsForm(request.POST)

        if form.is_valid():
                name_to_do_lists = form.save(commit=False)
                name_to_do_lists.owner = self.request.user
                name_to_do_lists.set_password(form.cleaned_data['password'])
                name_to_do_lists.save()
                return redirect('main:name_to_do_lists')



class NameToDoListsView(LoginRequiredMixin, View):
    template_name = 'main/name_to_do_list.html'

    def get(self, request) :
        name_to_do_lists = NameToDoLists.objects.all()

        ctx = {'name_to_do_lists' : name_to_do_lists}
        return render(request, self.template_name, ctx)




class NameToDoDeleteView(OwnerDeleteView):
    # Lets you delete a lesson.
    # Deleting a lesson does not affect any participation counts associated with the lesson.
    model = NameToDoLists

    def get_success_url(self):

        return reverse('main:name_to_do_lists')



class ToDoListCreateView(LoginRequiredMixin, View):

    def post(self, request, pk):
        form = ToDoListForm(request.POST)
        name_to_do_lists = get_object_or_404(NameToDoLists, pk=pk)

        if form.is_valid():
            to_do_list = form.save(commit=False)
            to_do_list.owner = self.request.user
            to_do_list.name_to_do_lists = name_to_do_lists
            to_do_list.save()

            response_data = {
                'pk': to_do_list.pk,
                'title': to_do_list.title,
                'owner': to_do_list.owner.username,
            }
            return JsonResponse(response_data)

        errors = {field: form.errors[field][0] for field in form.errors}
        return JsonResponse({'errors': errors}, status=400)





class ToDoListView(LoginRequiredMixin, View):
    template_name = 'main/to_do_list.html'

    def get(self, request, pk) :
        name_to_do_lists = get_object_or_404(NameToDoLists, pk=pk)
        ctx = {'name_to_do_lists': name_to_do_lists}

        return render(request, self.template_name, ctx)

    def post(self, request, pk):
        name_to_do_lists = get_object_or_404(NameToDoLists, pk=pk)
        form = ToDoListForm(initial={'name_to_do_lists': name_to_do_lists})
        password_entered = request.POST.get('password')

        if name_to_do_lists.check_password(password_entered):
            to_do_list = ToDoList.objects.filter(name_to_do_lists=name_to_do_lists)
            ctx = {'form': form, 'to_do_list': to_do_list, 'name_to_do_lists': name_to_do_lists}
            return render(request, self.template_name, ctx)

        else:
            return redirect('main:name_to_do_lists')




class ToDoDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        to_do_list = get_object_or_404(ToDoList, pk=pk)

        if not request.user.is_superuser and to_do_list.owner != request.user:
            return JsonResponse({'status': 'error', 'message': 'Permission denied'}, status=403)

        to_do_list.delete()

        response_data = {
            'status': 'success',
            'pk': pk,
        }
        return JsonResponse(response_data)