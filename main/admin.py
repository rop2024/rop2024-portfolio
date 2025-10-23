from django.contrib import admin
from django.utils.html import format_html
from .models import Profile, Project, ProjectRender, ContactMessage

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'email', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'title', 'bio', 'email', 'phone', 'location')
        }),
        ('Social Links', {
            'fields': ('github', 'linkedin', 'twitter', 'personal_website')
        }),
        ('Media', {
            'fields': ('profile_image', 'resume')
        }),
    )
    
    def has_add_permission(self, request):
        # Allow only one profile instance
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)

class ProjectRenderInline(admin.TabularInline):
    model = ProjectRender
    extra = 1
    fields = ('title', 'image', 'description', 'display_order')
    readonly_fields = ('created_at',)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        'title', 
        'project_type', 
        'is_featured', 
        'is_published', 
        'display_order',
        'created_at'
    )
    list_filter = ('project_type', 'is_featured', 'is_published', 'created_at')
    list_editable = ('is_featured', 'is_published', 'display_order')
    search_fields = ('title', 'description', 'technologies')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at', 'project_image_preview')
    
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'title', 
                'slug', 
                'short_description', 
                'description',
                'project_type'
            )
        }),
        ('Project Details', {
            'fields': (
                'technologies',
                'github_url',
                'live_url',
                'start_date',
                'end_date',
            )
        }),
        ('Media & Display', {
            'fields': (
                'featured_image',
                'project_image_preview',
                'display_order',
                'is_featured',
                'is_published',
            )
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [ProjectRenderInline]
    
    def project_image_preview(self, obj):
        if obj.featured_image:
            return format_html(
                '<img src="{}" width="150" height="100" style="object-fit: cover;" />',
                obj.featured_image.url
            )
        return "-"
    project_image_preview.short_description = "Image Preview"

@admin.register(ProjectRender)
class ProjectRenderAdmin(admin.ModelAdmin):
    list_display = ('project', 'title', 'display_order', 'created_at')
    list_filter = ('project', 'created_at')
    search_fields = ('project__title', 'title', 'description')
    list_editable = ('display_order',)
    readonly_fields = ('created_at', 'image_preview')
    
    fieldsets = (
        (None, {
            'fields': ('project', 'title', 'image', 'image_preview', 'description', 'display_order')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="150" height="100" style="object-fit: cover;" />',
                obj.image.url
            )
        return "-"
    image_preview.short_description = "Image Preview"

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'status', 'created_at')
    list_filter = ('status', 'is_archived', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    list_editable = ('status',)
    readonly_fields = (
        'name', 'email', 'subject', 'message', 'ip_address', 
        'user_agent', 'created_at', 'updated_at'
    )
    actions = ['mark_as_read', 'mark_as_replied', 'archive_messages']
    
    fieldsets = (
        ('Message Details', {
            'fields': ('name', 'email', 'subject', 'message')
        }),
        ('Technical Info', {
            'fields': ('ip_address', 'user_agent'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('status', 'is_archived')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def mark_as_read(self, request, queryset):
        updated = queryset.update(status='read')
        self.message_user(request, f'{updated} messages marked as read.')
    mark_as_read.short_description = "Mark selected messages as read"
    
    def mark_as_replied(self, request, queryset):
        updated = queryset.update(status='replied')
        self.message_user(request, f'{updated} messages marked as replied.')
    mark_as_replied.short_description = "Mark selected messages as replied"
    
    def archive_messages(self, request, queryset):
        updated = queryset.update(is_archived=True)
        self.message_user(request, f'{updated} messages archived.')
    archive_messages.short_description = "Archive selected messages"
    
    def has_add_permission(self, request):
        # Prevent adding messages through admin (they should come from contact form)
        return False
    
    def has_change_permission(self, request, obj=None):
        # Allow changing status but not message content
        return True
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ('name', 'email', 'subject', 'message')
        return self.readonly_fields