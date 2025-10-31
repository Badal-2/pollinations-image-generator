from django.db import models
from django.utils import timezone

class GeneratedImage(models.Model):
    prompt = models.TextField(help_text="Text prompt used to generate image")
    image = models.ImageField(upload_to='generated_images/', help_text="Generated image file")
    created_at = models.DateTimeField(default=timezone.now, help_text="When image was generated")
    image_url = models.URLField(max_length=500, blank=True, null=True, help_text="Direct URL from API")
    
    class Meta:
        ordering = ['-created_at']  # Newest first
        verbose_name = "Generated Image"
        verbose_name_plural = "Generated Images"
    
    def __str__(self):
        return f"{self.prompt[:50]}... - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
    
    def get_image_url(self):
        """Return image URL for frontend"""
        if self.image:
            return self.image.url
        return self.image_url