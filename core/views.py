import os
from io import BytesIO

import pandas
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser
from rest_framework.permissions import AllowAny, IsAuthenticated, BasePermission
from rest_framework.response import Response
from rest_framework.views import APIView
from core import serializers, models
from employee.settings import MEDIA_ROOT


class UserList(generics.ListCreateAPIView):
    """
        List and Create User
    """
    permission_classes = (AllowAny,)
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.all().order_by('username')

    def get(self, request, *args, **kwargs):
        """
            List all users with custom pagination
        """

        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
            create user details
            :param request: user details
            :param kwargs: NA
            :return: user details
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'data': serializer.data, 'message': 'Successfully created', 'status': status.HTTP_201_CREATED},
                status=status.HTTP_201_CREATED)
        return Response(
            {'errors': serializer.errors, 'status': status.HTTP_400_BAD_REQUEST},
            status=status.HTTP_400_BAD_REQUEST)


class EmployeeList(generics.ListCreateAPIView):
    """
        List all Employee
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.EmployeeSerializer
    queryset = models.Employee.objects.all().order_by('-id')

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class EmployeeDetailSerializer(APIView):
    """
    List and updates corresponding Employee DetailS details
    """
    permission_classes = (IsAuthenticated,)
    queryset = models.Employee.objects.all().order_by('id')
    serializer_class = serializers.EmployeeDetailSerializer

    @staticmethod
    def get_object(pk):
        """
        Fetch corresponding employee object
        :param pk: employee id
        :return: employee object
        """
        try:
            return models.Employee.objects.get(pk=pk)
        except ObjectDoesNotExist:
            raise Http404

    def get(self, request, **kwargs):
        """
        Fetch employee details
        :param request: NA
        :param kwargs: employee id
        :return: employee details
        """
        pk = kwargs.get('pk')
        book = self.get_object(pk)
        serializer = self.serializer_class(book)
        return Response(serializer.data)

    def put(self, request, **kwargs):
        """
        Updates employee details
        :param request: employee details
        :param kwargs: employee id
        :return: employee details
        """
        pk = kwargs.get('pk')
        book = self.get_object(pk)
        serializer = self.serializer_class(instance=book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'data': serializer.data, 'message': 'Successfully updated', 'status': status.HTTP_202_ACCEPTED},
                status=status.HTTP_202_ACCEPTED)
        return Response({'errors': serializer.errors, 'status': status.HTTP_400_BAD_REQUEST},
                        status.HTTP_400_BAD_REQUEST
                        )


class IsSuperAdminUser(BasePermission):
    """
    Allows access only to admin users.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class FileUpload(APIView):
    serializer_class = serializers.FileSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (IsSuperAdminUser,)
    queryset = models.CSVFile.objects.all().order_by('id')

    def post(self, request, *args, **kwargs):
        file_serializer = self.serializer_class(data=request.data)
        if file_serializer.is_valid():
            data = file_serializer.save()
            file_name = os.path.join(MEDIA_ROOT, str(data.file))
            data = pandas.read_csv(file_name)
            bulk_data = list(data.T.to_dict().values())
            for value in bulk_data:
                obj, created = models.Employee.objects.update_or_create(**value,
                                                                        defaults={'emp_code': value['emp_code']},
                                                                        )
            return Response({'message': 'Successfully Uploaded', 'status': status.HTTP_202_ACCEPTED})
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
