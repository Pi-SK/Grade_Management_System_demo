from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.core.paginator import Paginator
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.urls import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist

from .models import Student, Course, Score
from .forms import QueryForm_students, StudentForm, CourseForm, ScoreForm, QueryForm_grades, QueryForm_students, QueryForm_courses


def index(request):
    return render(request, "GradeManage/index.html")


#=====================================学生信息板块视图===========================================

# 新建学生视图
class StudentCreateView(CreateView):
    model = Student
    form_class = StudentForm
    success_url = reverse_lazy('GradeManage:student_list')
    template_name_suffix = '_create'
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # 如果是创建操作，不需要传递 instance
        if 'pk' not in self.kwargs:
            kwargs.pop('instance', None)
        return kwargs

# 修改学生信息视图
class StudentEditView(UpdateView):
    model = Student
    form_class = StudentForm
    success_url = reverse_lazy('GradeManage:student_list')
    template_name_suffix = '_edit'
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # 如果是创建操作，不需要传递 instance
        if 'pk' not in self.kwargs:
            kwargs.pop('instance', None)
        return kwargs

# 删除学生视图
class StudentDeleteView(DeleteView):
    model = Student
    success_url = reverse_lazy('GradeManage:student_list')
    template_name_suffix = '_delete'

# 展示学生信息视图
class StudentListView(ListView):
    model = Student
    paginate_by = 15
    template_name = 'GradeManage/student_list.html'


#=====================================课程信息板块视图===========================================

# 新建课程视图
class CourseCreateView(CreateView):
    model = Course
    form_class = CourseForm
    success_url = reverse_lazy('GradeManage:course_list')
    template_name_suffix = '_create'
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # 如果是创建操作，不需要传递 instance
        if 'pk' not in self.kwargs:
            kwargs.pop('instance', None)
        return kwargs

# 修改课程视图
class CourseEditView(UpdateView):
    model = Course
    form_class = CourseForm
    success_url = reverse_lazy('GradeManage:course_list')
    template_name_suffix = '_edit'
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # 如果是创建操作，不需要传递 instance
        if 'pk' not in self.kwargs:
            kwargs.pop('instance', None)
        return kwargs

# 删除课程视图
class CourseDeleteView(DeleteView):
    model = Course
    success_url = reverse_lazy('course_list')
    template_name_suffix = '_delete'

# 展示课程信息视图
class CourseListView(ListView):
    model = Course
    paginate_by = 15
    template_name = 'GradeManage/course_list.html'


#=====================================成绩信息板块视图===========================================

# 修改成绩视图
class GradeEditView(UpdateView):
    model = Score
    form_class = ScoreForm
    success_url = reverse_lazy('GradeManage:grade_index')
    template_name_suffix = '_edit'
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # 如果是创建操作，不需要传递 instance
        if 'pk' not in self.kwargs:
            kwargs.pop('instance', None)
        return kwargs

# 删除成绩视图
class GradeDeleteView(DeleteView):
    model = Score
    success_url = reverse_lazy('GradeManage:grade_index')
    template_name_suffix = '_delete'

# 学生成绩补录
class GradeCreateView(CreateView):
    model = Score
    form_class = ScoreForm
    success_url = reverse_lazy('GradeManage:score_create')
    template_name_suffix = '_create_stu'
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # 如果是创建操作，不需要传递 instance
        if 'pk' not in self.kwargs:
            kwargs.pop('instance', None)
        return kwargs


#=====================================筛选查询板块视图===========================================

# 成绩跨表查询，支持组合筛选
class QueryGradesListView(ListView):
    model = Score
    template_name = 'GradeManage/grade_index.html'
    context_object_name = 'grades'
    paginate_by = 15  # 设置每页显示的条目数量

    def get_queryset(self):
        form = QueryForm_grades(self.request.GET)
        if form.is_valid():
            student_id = form.cleaned_data.get('student_id')
            student_name = form.cleaned_data.get('student_name')
            course_id = form.cleaned_data.get('course_id')
            course_name = form.cleaned_data.get('course_name')
            major = form.cleaned_data.get('major')
            college = form.cleaned_data.get('college')

            queryset = Score.objects.all()
            # queryset = Score.objects.exclude(score=None)  # 过滤掉成绩为空的实例
            if student_id:
                queryset = queryset.filter(student__student_id=student_id)
            if student_name:
                queryset = queryset.filter(student__name__icontains=student_name)
            if course_id:
                queryset = queryset.filter(course__course_id=course_id)
            if course_name:
                queryset = queryset.filter(course__course_name__icontains=course_name)
            if major:
                queryset = queryset.filter(student__major=major)
            if college:
                queryset = queryset.filter(student__college=college)
            return queryset
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = QueryForm_grades(self.request.GET)
        # 将查询结果暂时储存
        context['queryset'] = self.queryset

        # 获取分页器对象
        paginator = context.get('paginator')
        # 获取当前页对象
        page_obj = context.get('page_obj')
        # 添加分页器对象和当前页对象到上下文中
        context['paginator'] = paginator
        context['page_obj'] = page_obj

        return context
    

# 学生信息查询，支持组合筛选
class QueryStudentsListView(ListView):
    model = Student
    template_name = 'GradeManage/student_list.html'
    context_object_name = 'students'
    paginate_by = 15

    def get_queryset(self):
        form = QueryForm_students(self.request.GET)
        if form.is_valid():
            student_id = form.cleaned_data.get('student_id')
            student_name = form.cleaned_data.get('student_name')
            major = form.cleaned_data.get('major')
            college = form.cleaned_data.get('college')

            queryset = Student.objects.all()
            if student_id:
                queryset = queryset.filter(student_id=student_id)
            if student_name:
                queryset = queryset.filter(name__icontains=student_name)
            if major:
                queryset = queryset.filter(major=major)
            if college:
                queryset = queryset.filter(college=college)
            return queryset
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = QueryForm_students(self.request.GET)

        # 获取分页器对象
        paginator = context.get('paginator')
        page_obj = context.get('page_obj')
        context['paginator'] = paginator
        context['page_obj'] = page_obj

        return context
    
    
# 课程信息查询，支持组合筛选
class QueryCoursesListView(ListView):
    model = Course
    template_name = 'GradeManage/course_list.html'
    context_object_name = 'courses'
    paginate_by = 15

    def get_queryset(self):
        form = QueryForm_courses(self.request.GET)
        if form.is_valid():
            course_id = form.cleaned_data.get('course_id')
            course_name = form.cleaned_data.get('course_name')
            credits = form.cleaned_data.get('credits')

            queryset = Course.objects.all()
            if course_id:
                queryset = queryset.filter(course_id=course_id)
            if course_name:
                queryset = queryset.filter(course_name__icontains=course_name)
            if credits:
                queryset = queryset.filter(credits=credits)
            return queryset
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = QueryForm_courses(self.request.GET)

        # 获取分页器对象
        paginator = context.get('paginator')
        page_obj = context.get('page_obj')
        context['paginator'] = paginator
        context['page_obj'] = page_obj

        return context
    

# =====================================名单导出工具===================================

from .utils import export_to_csv

# 导出学生信息为csv
def export_students_to_csv(request):
    import datetime
    from urllib.parse import quote

    fields = ['student_id', 'name', 'gender', 'birth_date', 'major', 'college']
    fields_names = ['学号', '姓名', '性别', '出生日期', '专业', '学院']

    # 给文件命名加上时间戳
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f'所有学生名单_{timestamp}.csv'
    filename = quote(filename)

    queryset = Student.objects.all()

    return export_to_csv(request, queryset, fields, filename, fields_names)


# 导出课程信息为csv
def export_courses_to_csv(request):
    import datetime
    from urllib.parse import quote

    fields = ['course_id', 'course_name', 'credits']
    fields_names = ['课程码', '课程名', '学分']

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f'所有课程名单_{timestamp}.csv'
    filename = quote(filename)

    queryset = Course.objects.all()

    return export_to_csv(request, queryset, fields, filename, fields_names)


# 导出成绩信息为csv
def export_scores_to_csv(request):
    import datetime
    from urllib.parse import quote

    fields = ['student__student_id', 'student__name', 'course__course_id', 'course__course_name', 'score', 'date']
    fields_names = ['学生学号', '学生姓名', '课程码', '课程名', '成绩', '日期']

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f'所有成绩名单_{timestamp}.csv'
    filename = quote(filename)

    queryset = Score.objects.all()

    return export_to_csv(request, queryset, fields, filename, fields_names)


# ====================================批量上传工具===================================

def upload_file_students(request):
    from .forms import UploadFileForm
    from .utils import save_temporary_file, import_csv_to_database
    from .models import Student
    from io import TextIOWrapper
    import csv
    
    url = 'GradeManage/student_upload.html'

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        #-------------
        if form.is_valid():
            csv_file = request.FILES['file']
            if not csv_file.name.endswith('.csv'):
                return render(request, url, {
                    'form': form,
                    'error': '上传的文件不是CSV格式！'
                })
            try:
                # 检查CSV文件内容格式
                text_file = TextIOWrapper(csv_file, encoding='utf-8-sig')
                reader = csv.reader(text_file)
                headers = next(reader)
                if headers != ['学号', '姓名', '性别', '出生日期', '专业', '学院']:
                    return render(request, url, {
                        'form': form,
                        'error': 'CSV文件内容格式不正确！'
                    })
                temp_file_path = save_temporary_file(csv_file)
                #-------------
                
                field_mapping = ['student_id', 'name', 'gender', 'birth_date', 'major', 'college']
                result = import_csv_to_database(temp_file_path, Student, field_mapping)
                
                return render(request, url, {'form': form, 'result': result})
            except Exception as e:
                return render(request, url, {
                    'form': form,
                    'error': '文件处理出错：' + str(e)
                })
    else:
        form = UploadFileForm()
    return render(request, url, {'form': form})


def upload_file_courses(request):
    from .forms import UploadFileForm
    from .utils import save_temporary_file, import_csv_to_database
    from .models import Course
    from io import TextIOWrapper
    import csv
    
    url = 'GradeManage/course_upload.html'

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        #-------------
        if form.is_valid():
            csv_file = request.FILES['file']
            if not csv_file.name.endswith('.csv'):
                return render(request, url, {
                    'form': form,
                    'error': '上传的文件不是CSV格式！'
                })
            try:
                # 检查CSV文件内容格式
                text_file = TextIOWrapper(csv_file, encoding='utf-8-sig')
                reader = csv.reader(text_file)
                headers = next(reader)
                if headers != ['课程码', '课程名', '学分']:
                    return render(request, url, {
                        'form': form,
                        'error': 'CSV文件内容格式不正确！'
                    })
                temp_file_path = save_temporary_file(csv_file)
                #-------------

                field_mapping = ['course_id', 'course_name', 'credits']
                result = import_csv_to_database(temp_file_path, Course, field_mapping)
                
                return render(request, url, {'form': form, 'result': result})
            except Exception as e:
                return render(request, url, {
                    'form': form,
                    'error': '文件处理出错：' + str(e)
                })
    else:
        form = UploadFileForm()
    return render(request, url, {'form': form})


def upload_file_grades(request):
    from .forms import UploadFileForm
    from .utils import save_temporary_file, import_csv_to_database
    from .models import Score
    from io import TextIOWrapper
    import csv
    
    url = 'GradeManage/grades_upload.html'

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        #-------------
        if form.is_valid():
            csv_file = request.FILES['file']
            if not csv_file.name.endswith('.csv'):
                return render(request, url, {
                    'form': form,
                    'error': '上传的文件不是CSV格式！'
                })
            try:
                # 检查CSV文件内容格式
                text_file = TextIOWrapper(csv_file, encoding='utf-8-sig')
                reader = csv.reader(text_file)
                headers = next(reader)
                if headers != ['课程', '学生', '成绩', '登记日期']:
                    return render(request, url, {
                        'form': form,
                        'error': 'CSV文件内容格式不正确！'
                    })
                temp_file_path = save_temporary_file(csv_file)
                #-------------

                field_mapping = ['course', 'student', 'score', 'date']
                result = import_csv_to_database(temp_file_path, Score, field_mapping)
                
                return render(request, url, {'form': form, 'result': result})
            except Exception as e:
                return render(request, url, {
                    'form': form,
                    'error': '文件处理出错：' + str(e)
                })
    else:
        form = UploadFileForm()
    return render(request, url, {'form': form})


# ==========================选课管理==============================

from django.http import JsonResponse
from django.utils import timezone
from decimal import Decimal
import json

def select_course_view(request):
    students = Student.objects.all()
    courses = Course.objects.all()
    return render(request, 'GradeManage/select_course.html', {
        'students': students,
        'courses': courses,
    })

def get_student_courses(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    selected_courses = student.scores.values_list('course_id', flat=True)
    print(selected_courses)
    return JsonResponse({
        'courses': list(selected_courses),
    })

import logging
logger = logging.getLogger(__name__)

def submit_courses(request):
    if request.method == 'POST':
        student_id_str = request.POST.get('student_id')
        course_ids_str = request.POST.getlist('courses[]')  
        student_id = Decimal(student_id_str)
        student = get_object_or_404(Student, student_id=student_id)
        
        selected_courses_set = set(course_ids_str)
        current_scores = student.scores.all()
        current_courses_set = {score.course_id for score in current_scores}
        
        # 添加日志记录来查看集合内容
        logger.error(f"Selected courses set: {selected_courses_set}")
        logger.error(f"Current courses set: {current_courses_set}")
        
        new_course_ids = selected_courses_set - current_courses_set
        
        logger.error(f"new_course_ids: {new_course_ids}")

        if not new_course_ids:
            logger.error("No new course IDs to add.")
            return JsonResponse({'error': '没有新的课程ID可以添加。'}, status=400)
        
        for course_id in new_course_ids:
            course = get_object_or_404(Course, course_id=course_id)
            logger.error(f"course: {course}")
            logger.error(f"student: {student}")
            try:
                Score.objects.create(student=student, course=course, score=None, date=timezone.now())
            except Exception as e:
                logger.exception("Exception occurred while creating a score record.")
                return JsonResponse({'error': str(e)}, status=400)
        
        return JsonResponse({'message': '选课成功', 'selected_courses': list(new_course_ids)})
    else:
        return JsonResponse({'error': '无效的请求'}, status=400)


#  ========================================成绩录入============================================

def score_create_select_course_view(request):
    students = Student.objects.all()
    courses = Course.objects.all()
    return render(request, 'GradeManage/score_create.html', {
        'students': students,
        'courses': courses,
    })


def get_students_by_course(request):
    if request.method == 'GET':
        course_id = request.GET.get('course_id', None)
        if course_id:
            # 获取选择了这门课的所有学生
            students = Score.objects.filter(course__course_id=course_id).values('student__student_id', 
                                                                                'student__name', 
                                                                                'student__major', 
                                                                                'student__college', 
                                                                                'student__gender', 
                                                                                'score')
            return JsonResponse(list(students), safe=False)
        else:
            return JsonResponse({'error': 'No course selected'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=405)
    

def update_scores(request):
    if request.method == 'POST':
        # 解析POST请求中的JSON数据
        scores_data = json.loads(request.body.decode('utf-8'))

        # 获取课程ID，假设它包含在JSON数据中
        course_id = scores_data.get('course_id')

        # 更新成绩
        for score_data in scores_data.get('scores', []):
            student_id = score_data['student_id']
            score = score_data['score']
            
            # 检查score是否为None或null字符串
            if score is None or score == 'null':
                # 选择跳过更新或设置一个默认值
                print(f"Score for student {student_id} in course {course_id} is None or 'null', skipping update.")
                continue
            
            try:
                # 获取Score模型实例，确保student_id和course_id的类型与数据库匹配
                score_obj = Score.objects.get(student__student_id=student_id, course__course_id=course_id)
                
                # 尝试将score转换为Decimal类型
                try:
                    score_decimal = Decimal(score)
                except (ValueError, TypeError):
                    # 如果转换失败，则打印错误信息并跳过
                    print(f"Invalid score value for student {student_id}: {score}")
                    continue
                
                # 更新成绩
                score_obj.score = score_decimal
                score_obj.save()
            except ObjectDoesNotExist:
                # 如果学生或课程不存在，记录错误并继续
                print(f"Score for student {student_id} in course {course_id} does not exist.")
                continue
        
        # 返回成功的响应
        return JsonResponse({'status': 'success'}, status=200)
    
    else:
        # 如果不是POST请求，返回错误响应
        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
    

# ======================================可视化工具====================================

def student_score_chart(request, student_id):
    student = Student.objects.get(student_id=student_id)
    scores = Score.objects.filter(student=student)
    course_names = [score.course.course_name for score in scores]
    scores = [str(score.score) for score in scores]  # 将Decimal对象转换为字符串
    return render(request, 'GradeManage/student_score_chart.html', {
        'student': student.name,
        'course_names': course_names,
        'scores': scores
    })


def course_score_chart(request, course_id):
    course = Course.objects.get(course_id=course_id) 
    scores = Score.objects.filter(course=course)
    course_names = [course.course_name for score in scores]
    student_names = [score.student.name for score in scores]
    scores = [str(score.score) for score in scores]  # 将Decimal对象转换为字符串
    return render(request, 'GradeManage/course_score_chart.html', {
        'student_names': student_names,
        'course_names': course_names,
        'scores': scores
    })


# ============================drafts ============================

# class ScoreCreateView(CreateView):
#     model = Score
#     form_class = ScoreForm

#     def form_valid(self, form):
#         try:
#             # 设置学生和日期
#             form.instance.student = self.student
#             form.instance.date = timezone.now()
#             # 保存表单
#             self.object = form.save()
#             return JsonResponse({'message': '选课成功', 'selected_courses': [form.instance.course.course_id]})
#         except Exception as e:
#             logger.exception("Exception occurred while creating a score record.")
#             return JsonResponse({'error': str(e)}, status=400)

#     def form_invalid(self, form):
#         return JsonResponse({'error': form.errors}, status=400)

# def submit_courses(request):
#     if request.method == 'POST':
#         student_id = request.POST.get('student_id')
#         course_ids_str = request.POST.getlist('courses[]')
#         student = get_object_or_404(Student, student_id=student_id)

#         selected_courses_set = set(course_ids_str)
#         current_scores = student.scores.all()
#         current_courses_set = {score.course_id for score in current_scores}

#         new_course_ids = selected_courses_set - current_courses_set

#         if not new_course_ids:
#             logger.error("No new course IDs to add.")
#             return JsonResponse({'error': '没有新的课程ID可以添加。'}, status=400)

#         for course_id in new_course_ids:
#             course = get_object_or_404(Course, course_id=course_id)
#             # 使用ScoreCreateView来创建分数记录
#             score_create_view = ScoreCreateView()
#             score_create_view.student = student
#             score_create_view.course = course
#             response = score_create_view.form_valid(ScoreForm(initial={'course': course, 'student': student}))
#             if response.status_code != 200:
#                 return response

#         return JsonResponse({'message': '选课成功', 'selected_courses': list(new_course_ids)})
#     else:
#         return JsonResponse({'error': '无效的请求'}, status=400)


# ### 导出筛选后的名单
# def export_filtered_grades_to_csv(request):
#     # 创建表单实例
#     form = QueryForm_grades(request.GET)
#     # 验证表单是否有效
#     if not form.is_valid():
#         # 如果表单无效，返回错误信息或处理其他逻辑
#         print("Form is not valid:", form.errors)
#         return HttpResponse("Invalid form data.")
#     # 定义要导出的字段，这些字段应该与Score模型直接相关或通过关系访问
#     fields = ['student__student_id', 'student__name', 'course__course_id', 'course__course_name', 'student__major', 'student__college']
#     field_names = ['学生学号', '学生姓名', '课程码', '课程名', '专业', '学院']
#     filename = 'filtered_grades.csv'

#     # 使用QueryGradesListView中的get_queryset方法来获取筛选后的数据集
#     query_view = QueryGradesListView()
#     query_view.request = request  # 需要手动设置request属性
#     queryset = query_view.get_queryset()

#     # 调用 export_to_csv 函数并返回响应
#     return export_to_csv(request, queryset, fields, filename, field_names)


# def export_filtered_students_to_csv(request):
#     # 定义要导出的字段，这些字段应该与Score模型直接相关或通过关系访问
#     fields = ['student_id', 'name', 'gender', 'birth_date', 'major', 'college']
#     field_names = ['学号', '姓名', '性别', '出生日期', '专业', '学院']
#     filename = 'filtered_students.csv'

#     query_view = QueryStudentsListView()
#     query_view.request = request  # 需要手动设置request属性
#     queryset = query_view.get_queryset()

#     print(queryset.query)

#     return export_to_csv(request, queryset, fields, filename, field_names)