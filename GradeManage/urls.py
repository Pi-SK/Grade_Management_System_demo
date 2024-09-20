from django.urls import path
from django.contrib import admin

from . import views

app_name = "GradeManage"
urlpatterns = [

    path("index/", views.index, name="index"),
    
    path('students/new/', views.StudentCreateView.as_view(), name='student_create'),
    path('students/<int:pk>/edit/', views.StudentEditView.as_view(), name='student_edit'),
    path('students/<int:pk>/delete/', views.StudentDeleteView.as_view(), name='student_delete'),
    path('students/', views.QueryStudentsListView.as_view(), name='student_list'),

    path('courses/new/', views.CourseCreateView.as_view(), name='course_create'),
    path('courses/<str:pk>/edit/edit/', views.CourseEditView.as_view(), name='course_edit'),
    path('courses/<str:pk>/delete/', views.CourseDeleteView.as_view(), name='course_delete'),
    path('courses/', views.QueryCoursesListView.as_view(), name='course_list'),

    path('grades/', views.QueryGradesListView.as_view(), name='grade_index'),
    path('grades/<int:pk>/edit/', views.GradeEditView.as_view(), name='grade_edit'),
    path('grades/<int:pk>/delete/', views.GradeDeleteView.as_view(), name='grade_delete'),

    path('students/export_students_to_csv/', views.export_students_to_csv, name="export_students_to_csv"),
    path('course/export_courses_to_csv/', views.export_courses_to_csv, name="export_courses_to_csv"),
    path('grades/export_grades_to_csv/', views.export_scores_to_csv, name="export_grades_to_csv"),
    
    path('students/upload/', views.upload_file_students, name='upload_file_students'),
    path('courses/upload/', views.upload_file_courses, name='upload_file_courses'),
    path('grades/upload_csv/', views.upload_file_grades, name='upload_file_grades'),

    path('select_course/', views.select_course_view, name='select_course'),
    path('get_student_courses/<int:student_id>/', views.get_student_courses, name='get_student_courses'),
    path('submit_courses/', views.submit_courses, name='submit_courses'),

    path('grades/new/', views.score_create_select_course_view, name='score_create'),
    path('get_students_by_course/', views.get_students_by_course, name='get_students_by_course'),
    path('update_scores/', views.update_scores, name='update_scores'),
    path('grades/new/stu', views.GradeCreateView.as_view(), name='score_create_stu'),

    path('student/<int:student_id>/score_chart/', views.student_score_chart, name='student_score_chart'),
    path('course/<str:course_id>/score_chart/', views.course_score_chart, name='course_score_chart'),
    
]