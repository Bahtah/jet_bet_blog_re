from django.contrib import admin

from article.models import Post, Category, FriendlyLink
from django_summernote.admin import SummernoteModelAdmin
from modeltranslation.admin import TabbedTranslationAdmin


@admin.register(Post)
class PostAdmin(SummernoteModelAdmin, TabbedTranslationAdmin):
    summernote_fields_es = ('content',)


@admin.register(Category)
class CategoryAdmin(TabbedTranslationAdmin):
    list_display = ['id', 'title']
    list_filter = ['title']
    search_fields = ['title']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(FriendlyLink)
class FriendlyLinkAdminAdmin(TabbedTranslationAdmin):
    list_display = ['friend', 'name', 'link']
    list_filter = ['name']
    search_fields = ['name']

