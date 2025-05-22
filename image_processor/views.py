from celery.result import AsyncResult
from rest_framework import viewsets, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from config.celery import app
from .models import Image
from .serializers import ImageSerializer, ImageCreateSerializer
from .tasks import compress_image, add


class TestSerializers(serializers.Serializer):
    id = serializers.UUIDField()


class ImageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling image upload and compression.
    """
    queryset = Image.objects.all().order_by('-created_at')
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action == 'create':
            return ImageCreateSerializer
        elif self.action == 'test2':
            return TestSerializers
        return ImageSerializer

    def perform_create(self, serializer):
        # Save the image
        image = serializer.save()

        # Trigger the Celery task to compress the image
        compress_image.delay(image.id)

        return image

    @action(detail=True, methods=['post'])
    def recompress(self, request, pk=None):
        """
        Action to recompress an image with a different quality.
        """
        image = self.get_object()

        # Get quality parameter from request data
        quality = request.data.get('quality', 60)
        try:
            quality = int(quality)
            if quality < 1 or quality > 100:
                return Response(
                    {"error": "Quality must be between 1 and 100"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except (ValueError, TypeError):
            return Response(
                {"error": "Quality must be a valid integer"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Reset status to pending
        image.status = 'pending'
        image.save(update_fields=['status'])

        # Trigger the Celery task with the specified quality
        compress_image.delay(image.id, quality)

        return Response(
            {"message": f"Image recompression queued with quality: {quality}%"},
            status=status.HTTP_202_ACCEPTED
        )

    @action(detail=False, methods=['get'])
    def test(self, request):
        a = add.delay(1, 2)
        return Response({"message": f"task_id {a.id}"})

    @action(detail=False, methods=['post'])
    def test2(self, request):
        serializer = TestSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = AsyncResult(str(serializer.validated_data['id']), app=app)
        print(result)
        if result.ready():
            return Response({"message": result.result})
        return Response({"message": f"processing"})
