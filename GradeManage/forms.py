from django import forms
from django_select2.forms import Select2Widget
from django.forms.widgets import DateInput, Select

from .models import Student, Course, Score


# ===================================基础信息表单========================================

class StudentForm(forms.ModelForm):
    gender = forms.ChoiceField(
    choices=(('男', '男'), ('女', '女')),
    widget=Select2Widget(attrs={'class': 'select2', 'style': 'width: 8rem;'}),
    label='性别'
    )

    class Meta:
        model = Student
        fields = ['student_id', 'name', 'birth_date', 'major', 'college', 'gender']
        labels = {
            'student_id': '学号',
            'name': '姓名',
            'gender': '性别',
            'birth_date': '出生日期',
            'major': '专业',
            'college': '学院',
        }

    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['student_id'].disabled = True
        else:
            self.fields['student_id'].disabled = False

        # 设置学号的输入类型为 text
        self.fields['student_id'].widget = forms.TextInput()
        self.fields['name'].widget = forms.TextInput()
        # 设置出生日期的输入类型为 date
        self.fields['birth_date'].widget = DateInput(attrs={'type': 'date'})
        self.fields['major'].widget = forms.TextInput()
        self.fields['college'].widget = forms.TextInput()
        
        if self.instance and self.instance.birth_date:
            self.initial['birth_date'] = self.instance.birth_date.strftime('%Y-%m-%d')


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['course_id', 'course_name', 'credits']
        labels = {
            'course_id': '课程码',
            'course_name': '课程名',
            'credits': '学分',
        }
    def __init__(self, *args, **kwargs):
        super(CourseForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['course_id'].disabled = True
        else:
            self.fields['course_id'].disabled = False


class ScoreForm(forms.ModelForm):
    course = forms.ModelChoiceField(
        queryset=Course.objects.all(),
        widget=Select2Widget(attrs={'class': 'select2', 'style': 'width: 8rem;'}),
        label='课程'
    )
    student = forms.ModelChoiceField(
        queryset=Student.objects.all(),
        widget=Select2Widget(attrs={'class': 'select2', 'style': 'width: 8rem;'}),
        label='学生'
    )

    class Meta:
        model = Score
        fields = ['course', 'student', 'score', 'date']
        labels = {
            'course': '课程',
            'student': '学生',
            'score': '成绩',
            'date': '登记日期',
        }

    def __init__(self, *args, **kwargs):
        super(ScoreForm, self).__init__(*args, **kwargs)
        self.fields['score'].required = False  # 分数可以为空
        self.fields['date'].required = False  # 日期可以自动设置
        # 检查是否为更新表单（即实例化表单时是否传递了instance）
        if 'instance' in kwargs and kwargs['instance'] is not None:
            # 禁用课程和学生字段的编辑
            self.fields['course'].disabled = True
            self.fields['student'].disabled = True
        else:
            # 在添加时，保持课程和学生字段可编辑
            self.fields['course'].disabled = False
            self.fields['student'].disabled = False

        self.fields['date'].widget = DateInput(attrs={'type': 'date'})
        if self.instance and self.instance.date:
            self.initial['date'] = self.instance.date.strftime('%Y-%m-%d')

            

# ===================================下拉列表查询========================================

class QueryForm_grades(forms.Form):
    # 学号下拉列表
    student_id_choices = [('', '---------')] + list(Student.objects.values_list('student_id', 'student_id'))
    student_id = forms.ChoiceField(
        choices=student_id_choices,
        required=False,
        widget=Select2Widget(attrs={'class': 'select2', 'data-placeholder': '不限学号', 'style': 'width: 8rem;'})
    )
    # 学生姓名下拉列表
    student_name_choices = [('', '---------')] + list(Student.objects.values_list('name', 'name'))
    student_name = forms.ChoiceField(
        choices=student_name_choices,
        required=False,
        widget=Select2Widget(attrs={'class': 'select2', 'data-placeholder': '不限学生姓名', 'style': 'width: 8rem;'})
    )
    # 课程号下拉列表
    course_id_choices = [('', '---------')] + list(Course.objects.values_list('course_id', 'course_id'))
    course_id = forms.ChoiceField(
        choices=course_id_choices,
        required=False,
        widget=Select2Widget(attrs={'class': 'select2', 'data-placeholder': '不限课程码', 'style': 'width: 8rem;'})
    )
    # 课程名下拉列表
    course_name_choices = [('', '---------')] + list(Course.objects.values_list('course_name', 'course_name'))
    course_name = forms.ChoiceField(
        choices=course_name_choices,
        required=False,
        widget=Select2Widget(attrs={'class': 'select2', 'data-placeholder': '不限课程名', 'style': 'width: 8rem;'})
    )
    # 专业下拉列表
    major_choices = [('', '---------')] + list(Student.objects.values_list('major', 'major').distinct())
    major = forms.ChoiceField(
        choices=major_choices,
        required=False,
        widget=Select2Widget(attrs={'class': 'select2', 'data-placeholder': '不限专业', 'style': 'width: 10rem;'})
    )
    # 学院下拉列表
    college_choices = [('', '---------')] + list(Student.objects.values_list('college', 'college').distinct())
    college = forms.ChoiceField(
        choices=college_choices,
        required=False,
        widget=Select2Widget(attrs={'class': 'select2', 'data-placeholder': '不限学院', 'style': 'width: 10rem;'})
    )


class QueryForm_students(forms.Form):
    # 学号下拉列表
    student_id_choices = [('', '---------')] + list(Student.objects.values_list('student_id', 'student_id'))
    student_id = forms.ChoiceField(
        choices=student_id_choices,
        required=False,
        widget=Select2Widget(attrs={'class': 'select2', 'data-placeholder': '不限学号', 'style': 'width: 8rem;'})
    )
    # 学生姓名下拉列表
    student_name_choices = [('', '---------')] + list(Student.objects.values_list('name', 'name'))
    student_name = forms.ChoiceField(
        choices=student_name_choices,
        required=False,
        widget=Select2Widget(attrs={'class': 'select2', 'data-placeholder': '不限学生姓名', 'style': 'width: 8rem;'})
    )
    # 专业下拉列表
    major_choices = [('', '---------')] + list(Student.objects.values_list('major', 'major').distinct())
    major = forms.ChoiceField(
        choices=major_choices,
        required=False,
        widget=Select2Widget(attrs={'class': 'select2', 'data-placeholder': '不限专业', 'style': 'width: 10rem;'})
    )
    # 学院下拉列表
    college_choices = [('', '---------')] + list(Student.objects.values_list('college', 'college').distinct())
    college = forms.ChoiceField(
        choices=college_choices,
        required=False,
        widget=Select2Widget(attrs={'class': 'select2', 'data-placeholder': '不限学院', 'style': 'width: 10rem;'})
    )


class QueryForm_courses(forms.Form):
    # 课程号下拉列表
    course_id_choices = [('', '---------')] + list(Course.objects.values_list('course_id', 'course_id'))
    course_id = forms.ChoiceField(
        choices=course_id_choices,
        required=False,
        widget=Select2Widget(attrs={'class': 'select2', 'data-placeholder': '不限课程码', 'style': 'width: 8rem;'})
    )
    # 课程名下拉列表
    course_name_choices = [('', '---------')] + list(Course.objects.values_list('course_name', 'course_name'))
    course_name = forms.ChoiceField(
        choices=course_name_choices,
        required=False,
        widget=Select2Widget(attrs={'class': 'select2', 'data-placeholder': '不限课程名', 'style': 'width: 8rem;'})
    )
    # 学分下拉列表
    credits_choices = [('', '---------')] + list(Course.objects.values_list('credits', 'credits').distinct())
    credits = forms.ChoiceField(
        choices=credits_choices,
        required=False,
        widget=Select2Widget(attrs={'class': 'select2', 'data-placeholder': '不限学分', 'style': 'width: 8rem;'})
    )


# ===================================文件上传========================================

class UploadFileForm(forms.Form):
    file = forms.FileField(
        label='选择CSV文件:',
        widget=forms.FileInput(attrs={
            'class': 'custom-file-input', 
            'accept': '.csv' # 限制文件类型
        })
    )

    