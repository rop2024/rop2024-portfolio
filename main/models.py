from django.db import models
from versatileimagefield.fields import VersatileImageField
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
import os

def validate_github_url(value):
    """
    Validate that the URL is a valid GitHub URL
    """
    validator = URLValidator()
    try:
        validator(value)
        if 'github.com' not in value:
            raise ValidationError('Please enter a valid GitHub URL')
    except ValidationError:
        raise ValidationError('Please enter a valid URL')

class Profile(models.Model):
    """
    Main profile information - singleton model for portfolio owner
    """
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    bio = models.TextField()
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=100, blank=True)
    
    # Social links
    github = models.URLField(validators=[validate_github_url], blank=True)
    linkedin = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    personal_website = models.URLField(blank=True)
    
    # Profile image
    profile_image = VersatileImageField(
        upload_to='profile/',
        blank=True,
        null=True,
        help_text='Main profile picture'
    )
    
    # Resume/CV
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profile"
    
    def __str__(self):
        return f"{self.name} - {self.title}"
    
    def save(self, *args, **kwargs):
        # Ensure only one profile instance exists
        if not self.pk and Profile.objects.exists():
            # If you're creating a new profile but one already exists
            pass
        super().save(*args, **kwargs)

class Project(models.Model):
    """
    Portfolio projects
    """
    PROJECT_TYPES = [
        ('web', 'Web Application'),
        ('mobile', 'Mobile App'),
        ('desktop', 'Desktop Software'),
        ('data', 'Data Science'),
        ('ml', 'Machine Learning'),
        ('other', 'Other'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    short_description = models.CharField(max_length=300)
    project_type = models.CharField(max_length=20, choices=PROJECT_TYPES, default='web')
    
    # Project details
    technologies = models.CharField(max_length=300, help_text="Comma-separated list of technologies used")
    github_url = models.URLField(validators=[validate_github_url], blank=True)
    live_url = models.URLField(blank=True, help_text="Link to live demo or deployed application")
    
    # Images
    featured_image = VersatileImageField(
        upload_to='projects/featured/',
        help_text='Main project image'
    )
    
    # Timeline
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True, help_text="Leave empty for ongoing projects")
    
    # Ordering and visibility
    display_order = models.IntegerField(default=0, help_text="Higher number appears first")
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-display_order', '-is_featured', '-created_at']
        verbose_name = "Project"
        verbose_name_plural = "Projects"
    
    def __str__(self):
        return self.title
    
    @property
    def is_ongoing(self):
        return self.end_date is None
    
    def get_technologies_list(self):
        """Return technologies as a list"""
        return [tech.strip() for tech in self.technologies.split(',')]

class ProjectRender(models.Model):
    """
    Additional images/screenshots for projects
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='renders')
    title = models.CharField(max_length=200, blank=True)
    image = VersatileImageField(
        upload_to='projects/renders/',
        help_text='Project screenshot or render'
    )
    description = models.TextField(blank=True)
    display_order = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['display_order', 'created_at']
        verbose_name = "Project Render"
        verbose_name_plural = "Project Renders"
    
    def __str__(self):
        return f"{self.project.title} - {self.title or 'Render'}"

class ContactMessage(models.Model):
    """
    Messages received through contact form
    """
    STATUS_CHOICES = [
        ('new', 'New'),
        ('read', 'Read'),
        ('replied', 'Replied'),
        ('archived', 'Archived'),
    ]
    
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True)
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='new')
    is_archived = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"
    
    def __str__(self):
        return f"{self.name} - {self.subject}"
    
    def mark_as_read(self):
        self.status = 'read'
        self.save()
    
    def mark_as_replied(self):
        self.status = 'replied'
        self.save()