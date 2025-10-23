from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Profile, Project, ProjectRender, ContactMessage

def home(request):
    try:
        profile = Profile.objects.first()
    except Profile.DoesNotExist:
        profile = None
    
    projects = Project.objects.filter(is_published=True).order_by('-display_order', '-created_at')[:6]
    featured_projects = Project.objects.filter(is_published=True, is_featured=True).order_by('-display_order', '-created_at')
    
    context = {
        'profile': profile,
        'projects': projects,
        'featured_projects': featured_projects,
    }
    return render(request, 'main/home.html', context)

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Get client IP and user agent
        ip_address = get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        
        # Create contact message
        ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message,
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        messages.success(request, 'Thank you for your message! I will get back to you soon.')
        return redirect('home')
    
    return redirect('home')

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip