from pickle import FALSE

from django.core.serializers import serialize
from django.db.models import Sum, Count, Q
from django.db.models.functions import Trunc
from django.shortcuts import get_object_or_404
from django.template.context_processors import request
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin, \
    DestroyModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet, ModelViewSet, GenericViewSet

from accounts.permissions import IsAdmin, IsOwner, IsMember
from accounts.serializers import UserSerializer
from task_manager.models import Project, Task
from task_manager.serializers import ProjectSerializers, ProjectDetailModelSerializer, \
    ProjectCreateAndUpdateSerializers, TaskSerializers, ProjectListSerializers, ProjectCreateSerializers, \
    ProjectUpdateSerializers, ProjectAddMemberSerializer


# from django.contrib.postgres.search import TrigramSimilarity


class FirstAPIView(APIView):
    def get(self, request):
        return Response(data={"message": "Hello World"})

    def post(self, request):
        data = request.data
        print(request)
        return Response(data=data)


class ProjectAPIView(APIView):
    def get(self, request, pk=None):
        if pk:
            p = get_object_or_404(Project, id=pk)
            serializer = ProjectDetailModelSerializer(p)
            return Response(serializer.data)
        else:
            projects = Project.objects.all()
            # data = []
            # for i in projects:
            #     p = {}
            #     p['id'] = i.id
            #     p['name'] = i.name
            #     p['description'] = i.description
            #     data.append(p)
            serializers = ProjectDetailModelSerializer(projects, many=True)
            return Response(serializers.data)

    def post(self, request):
        serializers = ProjectCreateAndUpdateSerializers(data=request.data)
        # 1
        # if serializers.is_valid():
        #     serializers.save()
        #     return Response(data=serializers.data)
        # return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
        # 2
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response(data=serializers.data)
        # 3
        # serializers.is_valid(raise_exception=True)
        # data = serializers.validated_data
        # p = Project.objects.create(
        #     name=data.get('name'),
        #     description=data.get('description')
        # )
        # serializers = ProjectSerializers(p)
        # return Response(data=serializers.data)

    def put(self, request, pk):
        project = get_object_or_404(Project, id=pk)
        serializer = ProjectCreateAndUpdateSerializers(data=request.data, instance=project)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        project = get_object_or_404(Project, id=pk)
        project.delete()
        return Response(data={"message": "deleted success"})


# class CustomPagination(PageNumberPagination):
#     page_size = 2
#     page_size_query_param = 'page_size'
#     max_page_size = 100


# class ProjectViewSet(ModelViewSet):
#     queryset = Project.objects.all()
#     serializer_class = ProjectSerializers
#     permission_classes = [IsAuthenticated, ]
#     filter_backends = [filters.SearchFilter]
#     search_fields = ['name', 'description']
#
#     # pagination_class = CustomPagination
#
#     def get_serializer_class(self):
#         if self.action in ['create', 'update']:
#             return ProjectCreateAndUpdateSerializers
#         elif self.action == 'retrieve':
#             return ProjectDetailModelSerializer
#         return self.serializer_class
#
#     def get_queryset(self):
#         # q = self.request.query_params.get('search')
#         queryset = self.queryset.annotate(total_task=Count('task_project'))
#         # if q:
#         # return queryset.annotate(s=TrigramSimilarity('name', q)).filter(s__gt=0.3).order_by('-s')
#         # return queryset.filter(Q(name__icontains=q) | Q(description__icontains=q))
#         return queryset
#
#     @action(methods=['get'], detail=True, url_path='project_task')
#     def tasks(self, request, pk=None):
#         project = get_object_or_404(Project, id=pk)
#         tasks = project.task_project.all()
#         serializer = TaskSerializers(tasks, many=True)
#         return Response(serializer.data)


# oddiy ViewSet
# def list(self, request):
#     projects = Project.objects.all()
#     serializers = ProjectSerializers(projects, many=True)
#     return Response(serializers.data)
#
# def retrieve(self, request, pk=None):
#     project = get_object_or_404(Project, id=pk)
#     serializer = ProjectDetailModelSerializer(project)
#     return Response(serializer.data)
#
# def create(self, request):
#     serializer = ProjectCreateAndUpdateSerializers(data=request.data)
#     serializer.is_valid(raise_exception=True)
#     serializer.save()
#     return Response(serializer.data)
#
# def update(self, request, pk=None):
#     project = get_object_or_404(Project, id=pk)
#     serializers = ProjectCreateAndUpdateSerializers(instance=project, data=request.data)
#     serializers.is_valid(raise_exception=True)
#     serializers.save()
#     return Response(serializers.data)
#
# def destroy(self, request, pk=None):
#     project = get_object_or_404(Project, id=pk)
#     project.delete()
#     return Response(data={"message": "success"})

class ProjectViewSetOptional(GenericViewSet, ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin,
                             DestroyModelMixin):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializers

    def get_queryset(self):
        return self.queryset.annotate(total_task=Count('task_project'))


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializers
    filter_backends = [DjangoFilterBackend]
    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filterset_fields = ['status', 'assign_to']
    pagination_class = None

    # def get_queryset(self):
    #     status = self.request.query_params.get('status')
    #     if status:
    #         return self.queryset.filter(status=status)
    #     return self.queryset

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy', 'partial_update']:
            return [IsAuthenticated(), IsAdmin()]
        return super(TaskViewSet, self).get_permissions()


class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectListSerializers
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        self.queryset = self.queryset.prefetch_related('members').select_related(
            'owner').annotate(total_task=Count('task_project'))
        if self.action in ['list', 'retrieve']:
            return self.queryset.filter(owner=self.request.user)
        elif self.action == 'my_project_member':
            return self.queryset.exclude(owner=self.request.user).filter(members__exact=self.request.user)
        return self.queryset

    def get_serializer_class(self):
        if self.action == 'create':
            return ProjectCreateSerializers
        elif self.action in ['update', "partial_update"]:
            return ProjectUpdateSerializers
        elif self.action == 'retrieve':
            return ProjectDetailModelSerializer
        return self.serializer_class

    # def get_permissions(self):
    #     if self.action == 'project_add_member':
    #         return [IsAuthenticated(), IsOwner()]
    #     return super(ProjectViewSet, self).get_permissions()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(methods=['get'], detail=False)
    def my_project_member(self, request):
        project = self.get_queryset()
        serializers = ProjectListSerializers(project, many=True)
        return Response(serializers.data)

    @action(methods=['put'], detail=True, serializer_class=ProjectAddMemberSerializer,
            permission_classes=[IsAuthenticated, IsOwner])
    def project_add_member(self, request, pk=None):
        project = self.get_object()
        serializers = ProjectAddMemberSerializer(data=request.data, instance=project, partial=True)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response(serializers.data)

    @action(methods=['get'], detail=True, permission_classes=[IsAuthenticated, IsMember | IsOwner])
    def project_members(self, request, pk=None):
        project = self.get_object()
        users = project.members.all()
        serializers = UserSerializer(users, many=True)
        return Response(serializers.data)
