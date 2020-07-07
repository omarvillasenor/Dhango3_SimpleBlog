from django.contrib import admin
from .models import Post, Comment
# Register your models here.

# admin.site.register(Post)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status') #To display the info on the list
    list_filter = ('status', 'created', 'publish', 'author') #To add a column and filter
    search_fields = ('title', 'body') #Searcheable attributes
    prepopulated_fields = {'slug': ('title',)} #To create te slug with the title
    raw_id_fields = ('author',) #Now, the Author filed is numeric and you can select your author
    date_hierarchy = 'publish' #To display a date relation up the list
    ordering = ('status', 'publish') #The criterion to order posts


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created','active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')