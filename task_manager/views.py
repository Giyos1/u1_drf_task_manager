from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from task_manager.models import Project
from task_manager.serializers import ProjectSerializers, ProjectModelSerializers


class FirstAPIView(APIView):
    def get(self, request):
        return Response(data={"message": "Hello World"})

    def post(self, request):
        data = request.data
        print(request)
        return Response(data=data)


# class ProjectAPIView(APIView):
#     def get(self, request):
#         projects = Project.objects.all()
#         # data = []
#         # for i in projects:
#         #     p = {}
#         #     p['id'] = i.id
#         #     p['name'] = i.name
#         #     p['description'] = i.description
#         #     data.append(p)
#         serializers = ProjectSerializers(projects, many=True)
#         return Response(serializers.data)
#
#     def post(self, request):
#         serializers = ProjectSerializers(data=request.data)
#         # 1
#         # if serializers.is_valid():
#         #     serializers.save()
#         #     return Response(data=serializers.data)
#         # return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
#         # 2
#         serializers.is_valid(raise_exception=True)
#         serializers.save()
#         return Response(data=serializers.data)
#         # 3
#         # serializers.is_valid(raise_exception=True)
#         # data = serializers.validated_data
#         # p = Project.objects.create(
#         #     name=data.get('name'),
#         #     description=data.get('description')
#         # )
#         # serializers = ProjectSerializers(p)
#         # return Response(data=serializers.data)
#
#     # def get(self, pk):
#     #     project = Project.objects.get(id=pk)
#     #     serializers = ProjectSerializers(instance=project)
#     #     return Response(data=serializers.data)
#     #
#     # def put(self, request, pk):
#     #     project = Project.objects.get(id=pk)
#     #     serializers = ProjectSerializers(instance=project, data=request.data)
#     #     serializers.is_valid(raise_exception=True)
#     #     serializers.save()
#     #     return Response(data=serializers.data)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Project
from .serializers import ProjectSerializers


class ProjectAPIView(APIView):

    def get(self, request, pk=None):
        if pk:
            project = get_object_or_404(Project, pk=pk)
            serializer = ProjectModelSerializers(project)
        else:
            projects = Project.objects.all()
            serializer = ProjectModelSerializers(projects, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProjectSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, pk=None):
        project = get_object_or_404(Project, pk=pk)
        serializer = ProjectModelSerializers(instance=project, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk=None):
        project = get_object_or_404(Project, pk=pk)
        project.delete()
        return Response({"message": "Project deleted"}, status=status.HTTP_204_NO_CONTENT)
