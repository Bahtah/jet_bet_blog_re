from modeltranslation.translator import register, TranslationOptions
from .models import Category, Post, FriendlyLink
from modeltranslation import settings

settings.AUTO_POPULATE = True


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(Post)
class PostTranslationOptions(TranslationOptions):
    fields = ('title', 'content',)


@register(FriendlyLink)
class FriendlyLinkTranslationOptions(TranslationOptions):
    fields = ('name',)
