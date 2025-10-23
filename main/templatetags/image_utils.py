from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def get_image_rendition(image, rendition_key):
    """
    Get a specific image rendition URL.
    
    Usage: {% get_image_rendition image 'medium' as image_url %}
    """
    if not image:
        return ""
    
    try:
        return getattr(image, rendition_key).url
    except (AttributeError, Exception):
        return image.url if image else ""

@register.simple_tag
def responsive_image(image, rendition_key, alt_text="", class_name="", lazy_loading=True, **kwargs):
    """
    Generate a responsive image tag with srcset and lazy loading.
    
    Usage:
        {% responsive_image project.featured_image 'medium' project.title 'w-full h-auto' %}
    """
    if not image:
        return ""
    
    try:
        # Get the specific rendition
        rendition = getattr(image, rendition_key)
        url = rendition.url
        width = getattr(rendition, 'width', '')
        height = getattr(rendition, 'height', '')
        
        # Generate srcset if available (from model properties)
        srcset = ""
        sizes = ""
        
        # Try to get srcset from model properties
        srcset_property = f"{rendition_key}_srcset"
        sizes_property = f"{rendition_key}_sizes"
        
        if hasattr(image, srcset_property):
            srcset = getattr(image, srcset_property, "")
        if hasattr(image, sizes_property):
            sizes = getattr(image, sizes_property, "")
        
        # Build image tag
        img_attrs = {
            'src': url,
            'alt': alt_text,
            'class': class_name,
        }
        
        # Only add width/height if they exist
        if width:
            img_attrs['width'] = width
        if height:
            img_attrs['height'] = height
            
        img_attrs['loading'] = 'lazy' if lazy_loading else 'eager'
        
        if srcset:
            img_attrs['srcset'] = srcset
        if sizes:
            img_attrs['sizes'] = sizes
            
        # Add any additional attributes
        img_attrs.update(kwargs)
        
        # Build the HTML
        attrs_str = " ".join([f'{key}="{value}"' for key, value in img_attrs.items()])
        return mark_safe(f'<img {attrs_str}>')
        
    except Exception as e:
        # Fallback to simple image tag
        return mark_safe(f'<img src="{image.url}" alt="{alt_text}" class="{class_name}" loading="lazy">')

@register.simple_tag
def picture_element(image, alt_text="", class_name="", lazy_loading=True):
    """
    Generate a <picture> element with multiple sources for better optimization.
    
    Usage:
        {% picture_element project.featured_image project.title 'w-full h-auto' %}
    """
    if not image:
        return ""
    
    try:
        # Generate different formats and sizes
        sources = []
        
        # WebP source (modern format)
        webp_srcset = []
        for size in ['small', 'medium', 'large']:
            try:
                rendition = getattr(image, size, None)
                if rendition:
                    webp_url = rendition.url.rsplit('.', 1)[0] + '.webp'
                    width = getattr(rendition, 'width', '')
                    webp_srcset.append(f"{webp_url} {width}w")
            except:
                continue
        
        if webp_srcset:
            sources.append(
                f'<source type="image/webp" srcset="{", ".join(webp_srcset)}">'
            )
        
        # Fallback JPEG/PNG source
        jpeg_srcset = []
        for size in ['small', 'medium', 'large']:
            try:
                rendition = getattr(image, size, None)
                if rendition:
                    width = getattr(rendition, 'width', '')
                    jpeg_srcset.append(f"{rendition.url} {width}w")
            except:
                continue
        
        if jpeg_srcset:
            sources.append(
                f'<source srcset="{", ".join(jpeg_srcset)}">'
            )
        
        # Fallback img tag
        loading_attr = 'loading="lazy"' if lazy_loading else ''
        fallback_img = f'<img src="{image.url}" alt="{alt_text}" class="{class_name}" {loading_attr}>'
        
        return mark_safe(f'<picture>{"".join(sources)}{fallback_img}</picture>')
        
    except Exception as e:
        # Fallback to simple image tag
        loading_attr = 'loading="lazy"' if lazy_loading else ''
        return mark_safe(f'<img src="{image.url}" alt="{alt_text}" class="{class_name}" {loading_attr}>')

@register.filter
def get_image_dimensions(image, rendition_key):
    """Get image dimensions for a specific rendition"""
    if not image:
        return (0, 0)
    
    try:
        rendition = getattr(image, rendition_key)
        width = getattr(rendition, 'width', 0)
        height = getattr(rendition, 'height', 0)
        return (width, height)
    except:
        width = getattr(image, 'width', 0)
        height = getattr(image, 'height', 0)
        return (width, height)