import pandas as pd

from datetime import datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import DataSource
from companies.models import Company
from emissions.models import EmissionRecord

from .utils import normalize_unit, calculate_emission


class UploadCSVView(APIView):

    def post(self, request):

        try:

            print("REQUEST RECEIVED")

            file = request.FILES.get('file')

            if not file:
                return Response(
                    {"error": "No file uploaded"},
                    status=400
                )

            source_type = request.data.get('source_type')

            company_id = request.data.get('company_id')

            print("COMPANY ID:", company_id)

            company = Company.objects.get(id=int(company_id))

            datasource = DataSource.objects.create(
                company=company,
                source_type=source_type,
                uploaded_file=file,
                status='PROCESSING'
            )

            file.seek(0)
            df = pd.read_csv(file)
            print(df.head())

            created_records = []

            for _, row in df.iterrows():

                value = float(row['activity_value'])

                unit = str(row['activity_unit'])

                normalized_value, normalized_unit = normalize_unit(
                    value,
                    unit
                )

                factor, co2e = calculate_emission(
                    row['category'],
                    normalized_value
                )

                flagged = False
                reason = ""
                if value < 0 or value > 10000:
                      flagged = True
                      reason = "Suspicious activity value"

                record = EmissionRecord.objects.create(
                    company=company,
                    source=datasource,

                    scope=row['scope'],
                    category=row['category'],

                    activity_date=datetime.strptime(
                        str(row['activity_date']),
                        "%Y-%m-%d"
                    ).date(),

                    activity_value=value,
                    activity_unit=unit,

                    normalized_value=normalized_value,
                    normalized_unit=normalized_unit,

                    emission_factor=factor,
                    co2e_emission=co2e,

                    is_flagged=flagged,
                    flag_reason=reason,

                    raw_data=row.to_dict()
                )

                created_records.append(record.id)

            datasource.status = 'COMPLETED'
            datasource.save()

            return Response({
                "message": "Upload successful",
                "records_created": len(created_records)
            })

        except Exception as e:

            print("ERROR:", str(e))

            return Response(
                {"error": str(e)},
                status=500
            )