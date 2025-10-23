from django.core.management.base import BaseCommand
from django.apps import apps
from versatileimagefield.image_warmer import VersatileImageFieldWarmer
from main.models import Project, Profile, ProjectRender
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Generate all image renditions for optimized loading'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--model',
            type=str,
            help='Specific model to optimize (Project, Profile, ProjectRender)',
        )
    
    def handle(self, *args, **options):
        models_to_optimize = []
        
        if options['model']:
            model_name = options['model']
            if model_name == 'Project':
                models_to_optimize = [Project]
            elif model_name == 'Profile':
                models_to_optimize = [Profile]
            elif model_name == 'ProjectRender':
                models_to_optimize = [ProjectRender]
            else:
                self.stdout.write(
                    self.style.ERROR(f'Unknown model: {model_name}')
                )
                return
        else:
            # Optimize all models
            models_to_optimize = [Project, Profile, ProjectRender]
        
        for model in models_to_optimize:
            self.optimize_model_images(model)
    
    def optimize_model_images(self, model):
        model_name = model.__name__
        self.stdout.write(f"Optimizing images for {model_name}...")
        
        # Define rendition sets based on model
        if model == Profile:
            rendition_key_set = 'profile_image'
            image_attr = 'profile_image'
        elif model == Project:
            rendition_key_set = 'project_featured'
            image_attr = 'featured_image'
        elif model == ProjectRender:
            rendition_key_set = 'project_gallery'
            image_attr = 'image'
        else:
            return
        
        # Get all instances with images
        queryset = model.objects.exclude(**{f'{image_attr}__isnull': True})
        queryset = queryset.exclude(**{image_attr: ''})
        
        total = queryset.count()
        self.stdout.write(f"Found {total} {model_name} instances with images")
        
        for i, instance in enumerate(queryset, 1):
            try:
                warmer = VersatileImageFieldWarmer(
                    instance_or_queryset=instance,
                    rendition_key_set=rendition_key_set,
                    image_attr=image_attr,
                    verbose=True
                )
                num_created, failed_to_create = warmer.warm()
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f'[{i}/{total}] {model_name} {instance}: '
                        f'Created {num_created} renditions'
                    )
                )
                
                if failed_to_create:
                    self.stdout.write(
                        self.style.WARNING(
                            f'Failed to create: {failed_to_create}'
                        )
                    )
                    
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f'Error processing {model_name} {instance}: {str(e)}'
                    )
                )