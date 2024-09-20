from django.contrib import admin

from .models import Student, Course, Score


class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'name', 'gender', 'birth_date', 'major', 'college')  
admin.site.register(Student, StudentAdmin)

class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_id', 'course_name', 'credits')  
admin.site.register(Course, CourseAdmin)

class ScoreAdmin(admin.ModelAdmin):
    list_display = ('course', 'student', 'score', 'date')
admin.site.register(Score, ScoreAdmin)
