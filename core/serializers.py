"""
    Following file contains all the serializer that are used in the Core application
"""
import csv

from rest_framework import serializers
from core import models
from django.utils.translation import gettext as _
from io import BytesIO
import pandas


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['id', 'email', 'first_name', 'password']
        extra_kwargs = {'password': {'write_only': True},
                        'id': {'read_only': True},
                        }

    def create(self, validated_data):
        password = self.remove_fields(validated_data, 'password')
        validated_data['username'] = validated_data['email']
        user = models.User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    @staticmethod
    def remove_fields(validated_data, field):
        return validated_data.pop(field)


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Employee
        fields = '__all__'


class EmployeeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Employee
        fields = '__all__'


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CSVFile
        fields = ('file',)

    def validate_file_data(self, data):
        error = {}
        csv_data = self.read_csv(data).fillna("")

        csv_filed = [f.name for f in models.Employee._meta.get_fields()[1:]]
        if csv_data.columns.size !=5:
            error['column_length'] = 'Invalid Header Length'
        if csv_data.values.size > 50:
            error['row_length'] = 'invalid rows,maximum of 20 rows'
        if len(set(csv_filed).union(set(csv_data.columns.values))) != 5:
            error['invalid_headers'] = 'invalid Headers'
        for i in [list(x) for x in csv_data.values]:
            if not all(i):
                error['empty_filed'] = 'empty value in csv'
        return error

    def read_csv(self, data):
        data = BytesIO(data.read())
        return pandas.read_csv(filepath_or_buffer=data)

    def validate_file(self, file):

        if (file.name.split('.')[-1]).lower() != 'csv':
            raise serializers.ValidationError(_('Invalid file type'))
        file_error = self.validate_file_data(file)
        if file_error:
            raise serializers.ValidationError(file_error)
        return file


