from django.shortcuts import render
from django.http import JsonResponse, FileResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
import json
from .utils import (
    generate_image_from_pollinations,
    save_generated_image,
    get_all_images,
    search_images_by_prompt,
    get_image_by_id
)


def index(request):
    return render(request, 'index.html')



@csrf_exempt
def generate_image(request):
    if request.method != 'POST':
        return JsonResponse({
            'success': False,
            'error': 'Only POST method allowed'
        }, status=405)
    
    try:
        # Parse request data
        data = json.loads(request.body)
        prompt = data.get('prompt', '').strip()
        
        if not prompt:
            return JsonResponse({
                'success': False,
                'error': 'Prompt cannot be empty'
            }, status=400)
        
        # Generate image using Pollinations.ai
        success, result, api_url = generate_image_from_pollinations(prompt)
        
        if not success:
            return JsonResponse({
                'success': False,
                'error': result
            }, status=500)
        
        # Save image to database
        saved_image = save_generated_image(prompt, result, api_url)
        if not saved_image:
            return JsonResponse({
                'success': False,
                'error': 'Failed to save image'
            }, status=500)
        
        # Return success response
        return JsonResponse({
            'success': True,
            'image_id': saved_image.id,
            'image_url': saved_image.get_image_url(),
            'prompt': saved_image.prompt,
            'created_at': saved_image.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        # Log the full error
        import traceback
        print("ERROR in generate_image:")
        print(traceback.format_exc())
        
        return JsonResponse({
            'success': False,
            'error': f'Server error: {str(e)}'
        }, status=500)


@require_http_methods(["GET"])
def get_gallery(request):
    """Get all images or search by prompt"""
    try:
        search_query = request.GET.get('search', '').strip()
        
        if search_query:
            images = search_images_by_prompt(search_query)
        else:
            images = get_all_images()
        
        # Prepare response data
        images_data = [
            {
                'id': img.id,
                'prompt': img.prompt,
                'image_url': img.get_image_url(),
                'created_at': img.created_at.strftime('%Y-%m-%d %H:%M:%S')
            }
            for img in images
        ]
        
        return JsonResponse({
            'success': True,
            'images': images_data,
            'count': len(images_data)
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Server error: {str(e)}'
        }, status=500)


@require_http_methods(["GET"])
def download_image(request, image_id):
    """Download specific image"""
    try:
        image = get_image_by_id(image_id)
        
        if not image or not image.image:
            raise Http404("Image not found")
        
        response = FileResponse(image.image.open('rb'), content_type='image/png')
        response['Content-Disposition'] = f'attachment; filename="generated_image_{image_id}.png"'
        
        return response
        
    except Exception as e:
        raise Http404("Image not found")