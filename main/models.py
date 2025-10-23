from django.db import models
from versatileimagefield.fields import VersatileImageField, PPOIField
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
    
    # Profile image with VersatileImageField
    profile_image = VersatileImageField(
        upload_to='profile/',
        blank=True,
        null=True,
        help_text='Main profile picture',
        ppoi_field='profile_image_ppoi',
        width_field='profile_image_width',
        height_field='profile_image_height',
    )
    profile_image_ppoi = PPOIField()  # Primary Point of Interest
    profile_image_width = models.PositiveIntegerField(blank=True, null=True)
    profile_image_height = models.PositiveIntegerField(blank=True, null=True)
    
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
    
    @property
    def profile_image_srcset(self):
        """Generate srcset for responsive profile images"""
        if not self.profile_image:
            return ""
        
        sizes = [
            ('small_square_crop', '150w'),
            ('medium_square_crop', '300w'),
            ('large_square_crop', '500w'),
        ]
        
        srcset = []
        for size, width in sizes:
            try:
                url = getattr(self.profile_image, size).url
                srcset.append(f"{url} {width}")
            except:
                continue
        
        return ", ".join(srcset)

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
    
    # Featured image with VersatileImageField
    featured_image = VersatileImageField(
        upload_to='projects/featured/',
        help_text='Main project image',
        ppoi_field='featured_image_ppoi',
        width_field='featured_image_width',
        height_field='featured_image_height',
    )
    featured_image_ppoi = PPOIField()
    featured_image_width = models.PositiveIntegerField(blank=True, null=True)
    featured_image_height = models.PositiveIntegerField(blank=True, null=True)
    
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
    
    @property
    def featured_image_srcset(self):
        """Generate srcset for responsive project images"""
        if not self.featured_image:
            return ""
        
        sizes = [
            ('small', '320w'),
            ('medium', '640w'),
            ('large', '1024w'),
            ('hero', '1600w'),
        ]
        
        srcset = []
        for size, width in sizes:
            try:
                url = getattr(self.featured_image, size).url
                srcset.append(f"{url} {width}")
            except:
                continue
        
        return ", ".join(srcset)
    
    @property
    def featured_image_sizes(self):
        """Generate sizes attribute for responsive images"""
        return "(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw"

class ProjectRender(models.Model):
    """
    Additional images/screenshots for projects
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='renders')
    title = models.CharField(max_length=200, blank=True)
    
    # Render image with VersatileImageField
    image = VersatileImageField(
        upload_to='projects/renders/',
        help_text='Project screenshot or render',
        ppoi_field='image_ppoi',
        width_field='image_width',
        height_field='image_height',
    )
    image_ppoi = PPOIField()
    image_width = models.PositiveIntegerField(blank=True, null=True)
    image_height = models.PositiveIntegerField(blank=True, null=True)
    
    description = models.TextField(blank=True)
    display_order = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['display_order', 'created_at']
        verbose_name = "Project Render"
        verbose_name_plural = "Project Renders"
    
    def __str__(self):
        return f"{self.project.title} - {self.title or 'Render'}"
    
    @property
    def image_srcset(self):
        """Generate srcset for responsive render images"""
        if not self.image:
            return ""
        
        sizes = [
            ('thumbnail', '100w'),
            ('card', '400w'),
            ('gallery', '800w'),
            ('lightbox', '1200w'),
        ]
        
        srcset = []
        for size, width in sizes:
            try:
                url = getattr(self.image, size).url
                srcset.append(f"{url} {width}")
            except:
                continue
        
        return ", ".join(srcset)
    
    @property
    def image_sizes(self):
        """Generate sizes attribute for responsive images"""
        return "(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 25vw"

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