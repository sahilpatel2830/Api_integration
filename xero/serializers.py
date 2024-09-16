from rest_framework import serializers

# Employee Create

class XeroEmployeeSerializer(serializers.Serializer):
    FirstName = serializers.CharField(max_length=100, required=True)
    LastName = serializers.CharField(max_length=100, required=True)