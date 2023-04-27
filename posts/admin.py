from django.contrib import admin

from .models import Post, Comment, IpModel


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'date', 'banner', 'draft')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    prepopulated_fields = {"slug": ("title",)}
    save_on_top = True
    save_as = True



class CommentInline(admin.TabularInline):
    model = Comment

class CommentAdmin(admin.ModelAdmin):
    inlines = [
        CommentInline,
    ]


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(IpModel)


