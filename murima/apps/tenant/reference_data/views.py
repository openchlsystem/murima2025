from rest_framework import generics
from .models import ReferenceDataType, ReferenceData, ReferenceDataHistory
from .serializers import (
    ReferenceDataTypeSerializer,
    ReferenceDataSerializer,
    ReferenceDataHistorySerializer
)


# ReferenceDataType Views
class ReferenceDataTypeListCreateView(generics.ListCreateAPIView):
    queryset = ReferenceDataType.objects.all()
    serializer_class = ReferenceDataTypeSerializer


class ReferenceDataTypeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ReferenceDataType.objects.all()
    serializer_class = ReferenceDataTypeSerializer


# ReferenceData Views
class ReferenceDataListCreateView(generics.ListCreateAPIView):
    queryset = ReferenceData.objects.all()
    serializer_class = ReferenceDataSerializer


class ReferenceDataDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ReferenceData.objects.all()
    serializer_class = ReferenceDataSerializer


# ReferenceDataHistory Views
class ReferenceDataHistoryListView(generics.ListAPIView):
    queryset = ReferenceDataHistory.objects.all()
    serializer_class = ReferenceDataHistorySerializer


class ReferenceDataHistoryDetailView(generics.RetrieveAPIView):
    queryset = ReferenceDataHistory.objects.all()
    serializer_class = ReferenceDataHistorySerializer
