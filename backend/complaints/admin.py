from django.contrib import admin
from .models import Complaint, Project, ComplaintType, Comment

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ('created_at',)
    fields = ('user', 'content', 'created_at')

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('complaint_code', 'title', 'project', 'status', 'registrant', 'created_at')
    list_filter = ('status', 'project', 'category', 'created_at')
    search_fields = ('title', 'description', 'complaint_code', 'customer_name')
    inlines = [CommentInline]
    readonly_fields = ('created_at', 'updated_at', 'complaint_code')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('complaint', 'user', 'content', 'created_at')
    list_filter = ('created_at', 'user')
    search_fields = ('content', 'complaint__title', 'user__username')
    readonly_fields = ('created_at',)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'created_at')
    search_fields = ('name', 'code')

@admin.register(ComplaintType)
class ComplaintTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
