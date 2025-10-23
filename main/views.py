from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView, FormView
from django.views.generic.edit import CreateView
from django.db.models import Count, Q
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils import timezone
from datetime import timedelta
from .models import Profile, Project, ProjectRender, ContactMessage
from .forms import ContactForm

class HomeView(TemplateView):
    """Homepage with featured projects and profile"""
    template_name = 'main/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['profile'] = Profile.objects.first()
        except Profile.DoesNotExist:
            context['profile'] = None
        
        # Get published projects ordered by display priority
        context['projects'] = Project.objects.filter(
            is_published=True
        ).order_by('-display_order', '-is_featured', '-created_at')[:6]
        
        context['featured_projects'] = Project.objects.filter(
            is_published=True, 
            is_featured=True
        ).order_by('-display_order', '-created_at')
        
        return context

class ProjectListView(ListView):
    """List all published projects"""
    model = Project
    template_name = 'main/projects/project_list.html'
    context_object_name = 'projects'
    paginate_by = 9
    
    def get_queryset(self):
        queryset = Project.objects.filter(is_published=True).order_by('-display_order', '-created_at')
        
        # Filter by project type if provided
        project_type = self.request.GET.get('type')
        if project_type:
            queryset = queryset.filter(project_type=project_type)
            
        # Search functionality
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(technologies__icontains=search_query)
            )
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project_types'] = Project.PROJECT_TYPES
        context['selected_type'] = self.request.GET.get('type', '')
        context['search_query'] = self.request.GET.get('q', '')
        
        # Count projects by type for filters
        context['project_counts'] = {
            project_type[0]: Project.objects.filter(
                is_published=True, 
                project_type=project_type[0]
            ).count()
            for project_type in Project.PROJECT_TYPES
        }
        
        return context

class ProjectDetailView(DetailView):
    """Project detail page with renders"""
    model = Project
    template_name = 'main/projects/project_detail.html'
    context_object_name = 'project'
    
    def get_queryset(self):
        return Project.objects.filter(is_published=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.get_object()
        
        # Get project renders ordered by display order
        context['renders'] = project.renders.all().order_by('display_order')
        
        # Get related projects (same type, excluding current)
        context['related_projects'] = Project.objects.filter(
            is_published=True,
            project_type=project.project_type
        ).exclude(id=project.id).order_by('-is_featured', '-display_order')[:3]
        
        return context

class RenderListView(ListView):
    """Grid view of all project renders"""
    model = ProjectRender
    template_name = 'main/renders/render_list.html'
    context_object_name = 'renders'
    paginate_by = 12
    
    def get_queryset(self):
        return ProjectRender.objects.filter(
            project__is_published=True
        ).select_related('project').order_by('project__display_order', 'display_order')

class ContactView(FormView):
    """Contact form view"""
    template_name = 'main/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        # Get client IP and user agent
        ip_address = self.get_client_ip()
        user_agent = self.request.META.get('HTTP_USER_AGENT', '')
        
        # Save the contact message
        contact_message = form.save(commit=False)
        contact_message.ip_address = ip_address
        contact_message.user_agent = user_agent
        contact_message.save()
        
        messages.success(
            self.request, 
            'Thank you for your message! I will get back to you soon.'
        )
        return super().form_valid(form)
    
    def get_client_ip(self):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['profile'] = Profile.objects.first()
        except Profile.DoesNotExist:
            context['profile'] = None
        return context

class StatsView(TemplateView):
    """Statistics dashboard with charts"""
    template_name = 'main/stats.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Basic counts
        context['total_projects'] = Project.objects.filter(is_published=True).count()
        context['total_renders'] = ProjectRender.objects.filter(project__is_published=True).count()
        context['total_contact_messages'] = ContactMessage.objects.count()
        context['featured_projects_count'] = Project.objects.filter(is_published=True, is_featured=True).count()
        
        # Projects by type
        context['projects_by_type'] = self.get_projects_by_type()
        
        # Technology usage
        context['technology_usage'] = self.get_technology_usage()
        
        # Monthly project creation stats
        context['monthly_project_stats'] = self.get_monthly_project_stats()
        
        # Contact message trends
        context['message_trends'] = self.get_message_trends()
        
        # Recent activity
        context['recent_projects'] = Project.objects.filter(
            is_published=True
        ).order_by('-created_at')[:5]
        
        context['recent_messages'] = ContactMessage.objects.all().order_by('-created_at')[:5]
        
        return context
    
    def get_projects_by_type(self):
        """Get project counts by type for pie chart"""
        projects_by_type = Project.objects.filter(
            is_published=True
        ).values('project_type').annotate(count=Count('id'))
        
        return {
            item['project_type']: item['count'] 
            for item in projects_by_type
        }
    
    def get_technology_usage(self):
        """Analyze technology usage across projects"""
        all_technologies = []
        projects = Project.objects.filter(is_published=True)
        
        for project in projects:
            tech_list = project.get_technologies_list()
            all_technologies.extend(tech_list)
        
        # Count technology usage
        from collections import Counter
        tech_counter = Counter(all_technologies)
        
        return dict(tech_counter.most_common(10))  # Top 10 technologies
    
    def get_monthly_project_stats(self):
        """Get project creation stats for the last 12 months"""
        from django.db.models.functions import TruncMonth
        from django.db.models import Count
        from datetime import datetime, timedelta
        
        one_year_ago = timezone.now() - timedelta(days=365)
        
        monthly_stats = Project.objects.filter(
            created_at__gte=one_year_ago
        ).annotate(
            month=TruncMonth('created_at')
        ).values('month').annotate(
            count=Count('id')
        ).order_by('month')
        
        # Format for Chart.js
        months = []
        counts = []
        
        for stat in monthly_stats:
            months.append(stat['month'].strftime('%b %Y'))
            counts.append(stat['count'])
        
        return {
            'labels': months,
            'data': counts
        }
    
    def get_message_trends(self):
        """Get contact message trends for the last 6 months"""
        from django.db.models.functions import TruncMonth
        from django.db.models import Count
        
        six_months_ago = timezone.now() - timedelta(days=180)
        
        message_trends = ContactMessage.objects.filter(
            created_at__gte=six_months_ago
        ).annotate(
            month=TruncMonth('created_at')
        ).values('month').annotate(
            count=Count('id')
        ).order_by('month')
        
        # Format for Chart.js
        months = []
        counts = []
        
        for trend in message_trends:
            months.append(trend['month'].strftime('%b %Y'))
            counts.append(trend['count'])
        
        return {
            'labels': months,
            'data': counts
        }

# Legacy function-based views for backward compatibility
def home(request):
    view = HomeView.as_view()
    return view(request)

def contact(request):
    view = ContactView.as_view()
    return view(request)