# ======================导出模型数据为csv===============================

def export_to_csv(request, queryset, fields, filename, custom_field_names=None):
    import csv
    from django.http import HttpResponse

    # 如果提供了自定义列名，则使用它们；否则使用 fields 列表
    field_names = custom_field_names if custom_field_names else fields

    # 创建 HttpResponse 对象，并指定编码格式为 UTF-8
    response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
    response['Content-Disposition'] = 'attachment; filename*=UTF-8\'\'{}'.format(filename)

    writer = csv.writer(response, quoting=csv.QUOTE_MINIMAL)  # 使用 QUOTE_MINIMAL 来避免不必要的引号
    writer.writerow(field_names)  # 写入自定义列名

    for obj in queryset:
        row = []
        for field in fields:
            # 如果字段包含 '__'，表示是跨关联模型的字段，需要特殊处理
            if '__' in field:
                related_fields = field.split('__')
                value = getattr(obj, related_fields[0])
                for related_field in related_fields[1:]:
                    value = getattr(value, related_field)
            else:
                value = getattr(obj, field)
            row.append(str(value))
        writer.writerow(row)

    return response


# ======================导入csv=============================

def save_temporary_file(file):
    from tempfile import NamedTemporaryFile
    with NamedTemporaryFile(delete=False, suffix='.csv') as temp_file:
        for chunk in file.chunks():
            temp_file.write(chunk)
        return temp_file.name

def import_csv_to_database(csv_file_path, model, field_mapping):
    import csv
    import os
    from django.db import models

    success_count = 0
    fail_count = 0
    fail_details = []

    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # 跳过标题行
        for row in reader:
            try:
                instance_data = {model_field: row[csv_index] for csv_index, model_field in enumerate(field_mapping)}
                instance, created = model.objects.update_or_create(
                    **{model._meta.pk.name: instance_data[model._meta.pk.name]},
                    defaults=instance_data
                )
                success_count += 1
            except Exception as e:
                fail_count += 1
                fail_details.append({'row': row, 'error': str(e)})

    os.unlink(csv_file_path)  # 删除临时文件
    return {
        'success_count': success_count,
        'fail_count': fail_count,
        'fail_details': fail_details
    }


# ======================drafts=============================

# def export_to_csv(model, fields, filename, custom_field_names=None, query=False):
#     import csv
#     from django.http import HttpResponse

#     # 如果提供了自定义列名，则使用它们；否则使用 fields 列表
#     field_names = custom_field_names if custom_field_names else fields

#     # 创建 HttpResponse 对象，并指定编码格式为 UTF-8
#     response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
#     response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)

#     writer = csv.writer(response, quoting=csv.QUOTE_MINIMAL)
#     writer.writerow(field_names)  # 写入自定义列名

#     if query:
#         # 这里我们复用QueryGradesListView中的get_queryset方法来获取筛选后的数据集
#         query_view = query
#         query_view.request = request  # 需要手动设置request属性
#         queryset = query_view.get_queryset()

#     queryset = model.objects.all()

#     # 获取模型的所有对象
#     for obj in queryset:
#         row = [str(getattr(obj, field)) for field in fields]  # 使用原始字段名获取数据
#         writer.writerow(row)

#     return response


# def import_csv_to_database(csv_file_path):
#     import csv
#     from .models import Student

#     success_count = 0
#     fail_count = 0
#     fail_details = []

#     with open(csv_file_path, mode='r', encoding='utf-8') as file:
#         reader = csv.reader(file)
#         next(reader)  # 跳过标题行
#         for row in reader:
#             try:
#                 student_id, name, gender, birth_date, major, college = row
#                 # 尝试创建或更新Student对象
#                 student, created = Student.objects.update_or_create(
#                     student_id=student_id,
#                     defaults={
#                         'name': name,
#                         'gender': gender,
#                         'birth_date': birth_date,  # 假设CSV中的日期格式是YYYY-MM-DD
#                         'major': major,
#                         'college': college,
#                     }
#                 )
#                 if created:
#                     success_count += 1
#                 else:
#                     success_count += 1  # 更新也视为成功
#             except Exception as e:
#                 fail_count += 1
#                 fail_details.append({'row': row, 'error': str(e)})

#     # 返回导入结果
#     return {
#         'success_count': success_count,
#         'fail_count': fail_count,
#         'fail_details': fail_details
#     }