from rest_framework.decorators import api_view
from rest_framework.response import Response
import pandas as pd


@api_view(['GET'])
def health_check(request):
    return Response({
        "status": "ok",
        "message": "Backend is working"
    })


@api_view(['POST'])
def upload_csv(request):
    if 'file' not in request.FILES:
        return Response(
            {"error": "No file uploaded"},
            status=400
        )

    file = request.FILES['file']

    try:
        df = pd.read_csv(file)
    except Exception as e:
        return Response(
            {"error": f"Invalid CSV file: {str(e)}"},
            status=400
        )

    required_columns = {'Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature'}
    if not required_columns.issubset(df.columns):
        return Response(
            {"error": "CSV missing required columns"},
            status=400
        )

  summary = {
    "total_equipment": int(len(df)),
    "average_flowrate": round(df['Flowrate'].mean(), 2),
    "average_pressure": round(df['Pressure'].mean(), 2),
    "average_temperature": round(df['Temperature'].mean(), 2),
    "equipment_type_distribution": df['Type'].value_counts().to_dict()
}


    return Response(summary)
