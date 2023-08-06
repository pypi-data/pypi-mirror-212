import json

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render


# Playground View
@login_required(login_url="/admin/login/")
def ussd_web_tester(request: HttpRequest):
    if request.method == "GET":
        return render(request, "splathash/index.html")

    # Echo service
    json_data = json.loads(request.body)
    msisdn = json_data["MSISDN"]
    user_id = json_data["USERID"]
    user_data = json_data["USERDATA"]
    message_type = json_data["MSGTYPE"]

    return JsonResponse(
        {
            "USERID": user_id,
            "MSISDN": msisdn,
            "MSG": f"Echo service is running. Your data: {user_data}",
            "MSGTYPE": message_type,
        }
    )
