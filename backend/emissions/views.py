from rest_framework.views import APIView
from rest_framework.response import Response

from .models import EmissionRecord
from .serializers import EmissionRecordSerializer

from rest_framework.permissions import IsAuthenticated

class EmissionListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        records = EmissionRecord.objects.all().order_by('-created_at')

        serializer = EmissionRecordSerializer(records, many=True)

        return Response(serializer.data)


class ApproveEmissionView(APIView):

    def post(self, request, pk):

        record = EmissionRecord.objects.get(id=pk)

        record.status = 'APPROVED'
        record.locked = True

        record.save()

        return Response({
            "message": "Record approved"
        })