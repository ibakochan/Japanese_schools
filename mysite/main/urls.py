from django.urls import path
from . import views
from django.contrib.auth.decorators import user_passes_test


def is_superuser(user):
    return user.is_superuser



app_name='main'
urlpatterns = [
    path('profile/<int:user_id>/', views.ProfilePageView.as_view(), name='profile'),
    path('profile/<int:user_id>/participation_count/', views.ParticipationCountView.as_view(), name='participation_count'),
    path('profile/picture/<int:user_id>/', user_passes_test(is_superuser)(views.profile_stream_file), name='profile_picture'),
    path('profile/<int:pk>/grading/', views.GradingView.as_view(), name='grading'),
    path('participation_increase/<int:user_id>/', views.ProfileParticipationIncreaseView.as_view(), name='profile_participation_increase'),
    path('grading/picture/<int:pk>/', user_passes_test(is_superuser)(views.grading_stream_file), name='grading_picture'),
    path('delete/<int:pk>/', views.AccountDeleteView.as_view(), name='delete_account'),
    path('set-user-limit/', views.SetUserLimitView.as_view(), name='set_user_limit'),

    path('', views.ScheduleListView.as_view(), name='schedules'),
    path('schedule/create/', views.ScheduleCreateView.as_view(), name='schedule_create'),
    path('schedule/<int:pk>/', views.ScheduleView.as_view(), name='schedule'),
    path('schedule/<int:pk>/update/', views.ScheduleUpdateView.as_view(), name='schedule_update'),
    path('schedule/picture/<int:pk>/', views.schedule_stream_file, name='schedule_picture'),
    path('schedule/<int:pk>/delete', views.ScheduleDeleteView.as_view(), name='schedule_delete'),

    path('lesson/<int:pk>/', views.LessonView.as_view(), name='lesson'),
    path('lesson/<int:pk>/update/', views.LessonUpdateView.as_view(), name='lesson_update'),
    path('schedule/<int:pk>/lesson/create/', views.NewLessonCreateView.as_view(), name='new_lesson_create'),
    path('lesson/picture/<int:pk>/', views.stream_file, name='lesson_picture'),
    path('lesson/<int:pk>/delete', views.LessonDeleteView.as_view(), name='lesson_delete'),
    path('add_users_to_lessons/', views.AddUsersToLessonsView.as_view(), name='add_users_to_lessons'),

    path('participation_increase/<int:pk>/<int:click_id>/', views.ParticipationIncreaseView.as_view(), name='participation_increase'),
    path('late/absence/form/<int:pk>', views.LateAbsenceFormView.as_view(), name='late_absence_form'),
    path('late/absence/<int:pk>', views.LateAbsenceView.as_view(), name='late_absence'),

    path('name_to_do_lists/', views.NameToDoListsView.as_view(), name='name_to_do_lists'),
    path('name_to_do_lists/create/', views.NameToDoListsCreateView.as_view(), name='name_to_do_lists_create'),
    path('to_do_list/<int:pk>/', views.ToDoListView.as_view(), name='to_do_list'),
    path('to_do_list/create/<int:pk>/', views.ToDoListCreateView.as_view(), name='to_do_list_create'),
    path('todo/<int:pk>/delete', views.ToDoDeleteView.as_view(), name='to_do_delete'),
    path('name_todo/<int:pk>/delete/', views.NameToDoDeleteView.as_view(), name='name_to_do_delete'),
]

