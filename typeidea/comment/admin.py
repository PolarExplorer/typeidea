from django.contrib import admin

from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('target', 'nickname', 'content', 'website', 'created_time')
    fields = ('target', 'content', 'nickname', 'status', 'website', 'email')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(CommentAdmin, self).save_model(request, obj, form, change)
