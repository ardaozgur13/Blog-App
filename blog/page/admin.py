from django.contrib import admin
from .models import Tag, UserProfile, UserPost, Comment, User, ChildComment

# Custom admin classes
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

class UserPostAdmin(admin.ModelAdmin):
    list_display = ['id', 'post_image', 'comment_count', 'get_tags']
    filter_horizontal = ['tag_category']
    
    def get_tags(self, obj):
        return ", ".join([tag.name for tag in obj.tag_category.all()])
    get_tags.short_description = 'Tags'

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user']

class ProfileInline(admin.StackedInline):
    model = UserProfile

class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ["username"]
    inlines = [ProfileInline]

# Register all models
admin.site.register(Tag, TagAdmin)
admin.site.register(UserPost, UserPostAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Comment)
admin.site.register(ChildComment)


# Handle User model
admin.site.unregister(User)
admin.site.register(User, UserAdmin)