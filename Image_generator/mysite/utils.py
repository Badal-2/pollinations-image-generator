import requests
from django.core.files.base import ContentFile
from .models import GeneratedImage
import uuid
from urllib.parse import quote





def generate_image_from_pollinations(prompt):
    """
    Call Pollinations.ai API to generate image
    """
    try:
        # Pollinations.ai endpoint
        encoded_prompt = quote(prompt)
        api_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"
        
        # Add parameters for better quality
        params = {
            'width': 1024,
            'height': 1024,
            'nologo': 'true'
        }
        
        # Make request
        response = requests.get(api_url, params=params, timeout=30)
        
        if response.status_code == 200:
            return True, response.content, api_url
        else:
            return False, f"API returned status code: {response.status_code}", None
            
    except requests.exceptions.Timeout:
        return False, "Request timed out. Please try again.", None
    except requests.exceptions.RequestException as e:
        return False, f"Network error: {str(e)}", None
    except Exception as e:
        return False, f"Unexpected error: {str(e)}", None


def save_generated_image(prompt, image_content, api_url):
    """
    Save generated image to database and media folder
    Returns: GeneratedImage instance or None
    """
    try:
        # Generate unique filename
        filename = f"{uuid.uuid4()}.png"
        
        # Create model instance
        generated_image = GeneratedImage(
            prompt=prompt,
            image_url=api_url
        )
        
        # Save image file
        generated_image.image.save(filename, ContentFile(image_content), save=True)
        
        return generated_image
        
    except Exception as e:
        print(f"Error saving image: {str(e)}")
        return None


def get_all_images():
    """
    Fetch all generated images (newest first)
    """
    return GeneratedImage.objects.all()


def search_images_by_prompt(search_query):
    """
    Search images by prompt text
    """
    return GeneratedImage.objects.filter(prompt__icontains=search_query)


def get_image_by_id(image_id):
    """
    Get specific image by ID
    """
    try:
        return GeneratedImage.objects.get(id=image_id)
    except GeneratedImage.DoesNotExist:
        return None