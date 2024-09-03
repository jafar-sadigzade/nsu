from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin as DefaultFlatPageAdmin
from django.contrib.flatpages.models import FlatPage

from main.forms import FlatPageForm
from main.models import HomePage, New, Comment, Contact, Event, Staff


@admin.register(HomePage)
class HomePageAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'image')
    search_fields = ('title', 'description')
    ordering = ['id']


@admin.register(New)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'status', 'short_content')
    search_fields = ('title', 'date', 'status')
    list_filter = ('date', 'status')
    date_hierarchy = 'date'
    ordering = ('-date',)

    actions = ['mark_as_published']

    def mark_as_published(self, request, queryset):
        queryset.update(status='published')

    mark_as_published.short_description = 'Seçilmiş xəbərləri yayımla'

    def short_content(self, obj):
        return obj.content[:50]

    short_content.short_description = 'Xəbər mətni qısa'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('news', 'user', 'content', 'date_posted')
    list_filter = ('news', 'user', 'date_posted')
    search_fields = ('news__title', 'user__username', 'content')
    ordering = ['-date_posted']
    date_hierarchy = 'date_posted'

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('news', 'user')
        return queryset


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'email', 'phone_number', 'subject', 'created_date')
    list_filter = ('created_date',)
    search_fields = ('first_name', 'email', 'phone_number', 'subject', 'content')
    ordering = ['-created_date']
    date_hierarchy = 'created_date'

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset


admin.site.unregister(FlatPage)


@admin.register(FlatPage)
class FlatPageAdmin(DefaultFlatPageAdmin):
    form = FlatPageForm


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date',)
    search_fields = ('title', 'date',)
    list_filter = ('date',)
    date_hierarchy = 'date'
    ordering = ('-date',)


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('name', 'position')
    search_fields = ('name', 'position')
    list_filter = ('position',)
    ordering = ('name',)
