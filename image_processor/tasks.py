from PIL import Image as PILImage
from io import BytesIO
import os

from celery import shared_task
from django.core.files.base import ContentFile
from config.celery import app
from .models import Image
import logging

logger = logging.getLogger(__name__)


@app.task(name="compress_image")
def compress_image(image_id, quality=60):
    """
    Celery task for compressing an uploaded image.
    
    Args:
        image_id: ID of the Image model instance
        quality: Image quality after compression (1-100)
    """
    try:
        # Get the image object
        image_obj = Image.objects.get(id=image_id)

        # Update status to processing
        image_obj.status = 'processing'
        image_obj.save(update_fields=['status'])

        # Open the original image using PIL
        img = PILImage.open(image_obj.original_image.path)

        # Create a BytesIO object to store the compressed image
        buffer = BytesIO()

        # Save the image with compression
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        # Get original file size
        original_size = os.path.getsize(image_obj.original_image.path)

        # Save with compression
        img.save(
            buffer,
            format="JPEG",
            quality=quality,
            optimize=True
        )

        # Get the compressed file size
        buffer.seek(0)
        compressed_data = buffer.getvalue()
        compressed_size = len(compressed_data)

        # Calculate compression ratio
        compression_ratio = (original_size - compressed_size) / original_size * 100

        # Save the compressed image to the model
        buffer.seek(0)
        image_filename = os.path.basename(image_obj.original_image.name)
        filename, _ = os.path.splitext(image_filename)
        compressed_filename = f"{filename}_compressed.jpg"

        image_obj.compressed_image.save(
            compressed_filename,
            ContentFile(buffer.getvalue()),
            save=False
        )

        # Update image object with compression details
        image_obj.compression_ratio = compression_ratio
        image_obj.status = 'completed'
        image_obj.save()

        logger.info(f"Image {image_id} compressed successfully. Compression ratio: {compression_ratio:.2f}%")
        return f"Image compressed successfully. Compression ratio: {compression_ratio:.2f}%"

    except Image.DoesNotExist:
        logger.error(f"Image with ID {image_id} not found")
        return f"Image with ID {image_id} not found"
    except Exception as e:
        # If any errors occur, update status to failed
        try:
            image_obj = Image.objects.get(id=image_id)
            image_obj.status = 'failed'
            image_obj.save(update_fields=['status'])
        except:
            pass

        logger.error(f"Error compressing image {image_id}: {str(e)}")
        return f"Error compressing image: {str(e)}"


@shared_task
def add():
    print('salom')
