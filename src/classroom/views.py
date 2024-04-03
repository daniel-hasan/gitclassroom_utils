from ast import Assign
from django.shortcuts import render
from .models import Assignment
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import get_object_or_404

# Create your views here.

def allow_cors(json_response):
    json_response["Access-Control-Allow-Origin"] = "*"
    json_response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    json_response["Access-Control-Max-Age"] = "1000"
    json_response["Access-Control-Allow-Headers"] = "Content-Type, X-Requested-With, Content-Type"
    return json_response
import json
from datetime import datetime
from django.utils.timezone import make_aware
def get_discipline_assignments(request, discipline_name):

    lst_assignments = list(Assignment.objects.filter(discipline_fk__name = discipline_name)\
                            .values("acronym", "assignment_url","invitation_url",
                                        "deadline"))


    response = JsonResponse({"assignments": lst_assignments
                           }, status=200) 

    return allow_cors(response)

@csrf_exempt 
def update_assignments(request, discipline_name):
    arr_updated = []
    arr_not_updated = []
    arr_discipline_schedule = json.load(request)["dados_cronograma"]

    for discipline_schedule in arr_discipline_schedule:
        updated = False
        str_date_id = discipline_schedule["desc"]
        print(str_date_id)
        if "timestamp_data" in discipline_schedule:
            data = datetime.fromtimestamp(discipline_schedule["timestamp_data"])
            str_date_id = data.strftime("%d/%m")

        if "sigla_assignment" in discipline_schedule and "timestamp_entrega" in discipline_schedule:
            str_date_id = discipline_schedule["sigla_assignment"]
            try:
                assignment = Assignment.objects\
                            .get(discipline_fk__name = discipline_name,
                                acronym = discipline_schedule["sigla_assignment"])
                deadline = datetime.fromtimestamp(discipline_schedule["timestamp_entrega"])
                deadline = make_aware(deadline.replace(hour=23, minute=59))

                assignment.deadline = deadline
                assignment.save()
                updated = True
            except Assignment.DoesNotExist:
                pass

        if updated:
            arr_updated.append(str_date_id)
        else:
            arr_not_updated.append(str_date_id)

    response = JsonResponse({"updated": arr_updated,
                            "not_updated": arr_not_updated}, status=200)

    return allow_cors(response)