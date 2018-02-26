from django.shortcuts import render_to_response
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from datetime import datetime
import json

from .models import Event, Member, Cost
from .slack import Slack, SlackMessage

# Create your views here.
def index(request):
    return render_to_response('index.html')

def last(request):
    n = request.GET.get('n')
    try:
        n = int(n)
    except:
        n = 1

    costs = Cost.get_costs_json(Event.get_last_N(n))
    return JsonResponse({'result': costs})

def members(request):
    members = Member.get_members_json()
    return JsonResponse({'result': members})

def this_week(request):
    costs = Cost.get_costs_json(Event.get_this_week())
    return JsonResponse({'result': costs})

def this_month(request):
    costs = Cost.get_costs_json(Event.get_this_month())
    return JsonResponse({'result': costs})

def this_year(request):
    costs = Cost.get_costs_json(Event.get_this_year())
    return JsonResponse({'result': costs})

@csrf_exempt
def new_report(request):
    data = json.loads(request.body)
    restaurantName = data.get('restaurant')
    if restaurantName == None:
        restaurantName = "" # for recharge case

    eventTime = data.get('time') #2018-01-09
    try:
        eventTime = datetime.strptime(eventTime, '%Y-%m-%d')
    except:
        eventTime = datetime.now()

    records = data.get('records')
    if records == None:
        return JsonResponse({'error': 'missing records'})

    result, errorMessage = Event.submit(restaurantName, eventTime, records)
    if not result:
        return JsonResponse({'error': errorMessage})

    message = SlackMessage.events_message(Event.get_last_N(1))
    Slack.post(message)

    return JsonResponse({'result': 'done'})

