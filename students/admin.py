from django.contrib import admin
from .models import Lesson,Homework,Davomat,Homeworkcheck

class Homeworkcheck(admin.StackedInline):
    model=Homeworkcheck
    extra=1


@admin.register(Homework)
class Homework(admin.ModelAdmin):
    list_display = ('lesson', 'team', 'homework_file','date')
    list_display_links = ('lesson',)
    search_fields = ('lesson',)
    inlines = [
        Homeworkcheck,
    ]

admin.site.register(Lesson)
admin.site.register(Davomat)
