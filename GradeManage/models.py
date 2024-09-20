from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator


class Student(models.Model):
    student_id = models.DecimalField(max_digits=8, decimal_places=0, primary_key=True)  # 学号
    name = models.CharField(max_length=20)  # 姓名
    gender = models.CharField(max_length=4, choices=[('男', '男'), ('女', '女')])  # 性别
    birth_date = models.DateField()  # 出生日期
    major = models.CharField(max_length=20)  # 专业
    college = models.CharField(max_length=20)  # 学院

    def __str__(self):
        return self.name


class Course(models.Model):
    course_id = models.CharField(max_length=8, primary_key=True)
    course_name = models.CharField(max_length=20)
    credits = models.DecimalField(max_digits=3, decimal_places=1)

    # 自定义验证器，确保课程号前四位是类别代号，后四位是顺序号
    course_id_validator = RegexValidator(
        regex=r'^(JCKC|ZYBX|ZYXX|BYSJ)\d{4}$',
        message='课程号格式错误，应为类别代号(JCKC:基础课程|ZYBX:专业必修|ZYXX:专业选修|BYSJ:毕业设计)后跟四位数字(例如: JCKC0001)'
    )

    def __str__(self):
        return self.course_name

    # 将验证器添加到course_id字段
    course_id = models.CharField(
        max_length=8,
        primary_key=True,
        validators=[course_id_validator]
    )


class Score(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='scores')  # 学号
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='scores')  # 课程号
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # 成绩
    date = models.DateField(default=timezone.now, null=True, blank=True)  # 日期，默认为当前日期

    class Meta:
        unique_together = ('student', 'course')  # 确保每个学生和课程组合是唯一的

    def __str__(self):
        return f"{self.student.student_id} - {self.course.course_id}"
