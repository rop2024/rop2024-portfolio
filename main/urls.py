from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.HomeView.as_view(), name='home'),
    
    # Projects
    path('projects/', views.ProjectListView.as_view(), name='project_list'),
    path('projects/<slug:slug>/', views.ProjectDetailView.as_view(), name='project_detail'),
    
    # Renders
    path('renders/', views.RenderListView.as_view(), name='render_list'),
    
    # Contact
    path('contact/', views.ContactView.as_view(), name='contact'),
    
    # Stats
    path('stats/', views.StatsView.as_view(), name='stats'),
]