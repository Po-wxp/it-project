from django.contrib import admin
from capturer.models import Category, Tag, Photo, UserProfile, Review, Contact
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = { 'slug' : ('name',)}

# admin.site.register(Category)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag)
admin.site.register(Photo)
admin.site.register(UserProfile)
admin.site.register(Review)
admin.site.register(Contact)


