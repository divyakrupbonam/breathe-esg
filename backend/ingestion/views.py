import pandas as pd

from datetime import datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import DataSource
from companies.models import Company
from emissions.models import EmissionRecord

from .utils import normalize_unit, calculate_emission


class UploadCSVView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        try:
            file = request.FILES.get('file')

            if not file:
                return Response({"error": "No file uploaded"}, status=400)

            source_type = request.data.get('source_type')
            company_id = request.data.get('company_id')

            if not company_id:
                return Response({"error": "company_id missing"}, status=400)

            company = Company.objects.get(id=int(company_id))

            datasource = DataSource.objects.create(
                company=company,
                source_type=source_type,
                uploaded_file=file,
                status='PROCESSING'
            )

            df = pd.read_csv(file)

            created_records = []

            for _, row in df.iterrows():
                value = float(row.get('activity_value', 0))
                unit = str(row.get('activity_unit', ''))

                normalized_value, normalized_unit = normalize_unit(value, unit)

                factor, co2e = calculate_emission(
                    row.get('category', ''),
                    normalized_value
                )

                flagged = value < 0 or value > 10000

                EmissionRecord.objects.create(
                    company=company,
                    source=datasource,
                    scope=row.get('scope', ''),
                    category=row.get('category', ''),
                    activity_date=datetime.strptime(str(row.get('activity_date')), "%Y-%m-%d").date(),
                    activity_value=value,
                    activity_unit=unit,
                    normalized_value=normalized_value,
                    normalized_unit=normalized_unit,
                    emission_factor=factor,
                    co2e_emission=co2e,
                    is_flagged=flagged,
                    flag_reason="Suspicious activity value" if flagged else "",
                    raw_data=row.to_dict()
                )
                

            datasource.status = 'COMPLETED'
            datasource.save()

            return Response({
                "message": "Upload successful",
                "records_created": len(created_records)
            })

        except Exception as e:
            print("ERROR:", str(e))
            return Response({"error": str(e)}, status=500)