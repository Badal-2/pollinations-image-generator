from django.contrib import admin
from .models import GeneratedImage

@admin.register(GeneratedImage)
class GeneratedImageAdmin(admin.ModelAdmin):
    list_display = ('short_prompt', 'created_at', 'image_preview')
    list_filter = ('created_at',)
    search_fields = ('prompt',)
    readonly_fields = ('created_at', 'image_preview')
    ordering = ('-created_at',)
    
    def short_prompt(self, obj):
        return obj.prompt[:50] + '...' if len(obj.prompt) > 50 else obj.prompt
    short_prompt.short_description = 'Prompt'
    
    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="200" height="200" style="object-fit: cover;" />'
        return 'No image'
    image_preview.short_description = 'Preview'
    image_preview.allow_tags = True