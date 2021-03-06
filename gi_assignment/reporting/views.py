from django.http import JsonResponse, HttpResponseBadRequest
import requests
from datetime import datetime
import math
from django.core.cache import cache
import json


def total_numbers(request, start_date, end_date):
    # Fetch API access token
    auth_token = request.META.get('HTTP_X_GI_TOKEN')
    if not auth_token:
        return HttpResponseBadRequest('Missing header "X-Gi-Token: b64-auth-token"')

    # Check if request is cached
    cache_key = '{}:{}:{}'.format(auth_token, start_date, end_date)
    if cache.get(cache_key) is not None:
        stats = json.loads(cache.get(cache_key))
    else:
        # Retrieve data from reporting API
        r = requests.get('https://api.gi'
                         'osg.com/api/reporting/v1/rooms/'
                         '84e0fefa-5675-11e7-a349-00163efdd8db/chat-stats/daily/'
                         '?start_date={}'
                         '&end_date={}'.format(start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")),
                         headers={
                             'Authorization': 'Token '+auth_token
                         })
        if r.status_code == 401:
            return HttpResponseBadRequest('Unauthorized')

        # Save this request-response to cache
        stats = r.json()
        cache.set(cache_key, json.dumps(stats), timeout=None)  # Infinite expiration time

    # Return total numbers as JSON
    return JsonResponse({
        'total_conversation_count': stats['total_conversation_count'],
        'total_user_message_count': stats['total_user_message_count'],
        'total_visitor_message_count': stats['total_visitor_message_count']
    })


def daily_numbers(request, start_date, end_date, page=1):
    # Fetch API access token
    auth_token = request.META.get('HTTP_X_GI_TOKEN')
    if not auth_token:
        return HttpResponseBadRequest('Missing header "X-Gi-Token: b64-auth-token"')

    # Check if request is cached
    cache_key = '{}:{}:{}'.format(auth_token, start_date, end_date)
    if cache.get(cache_key) is not None:
        stats = json.loads(cache.get(cache_key))
    else:
        # Retrieve data from reporting API
        r = requests.get('https://api.gi'
                         'osg.com/api/reporting/v1/rooms/'
                         '84e0fefa-5675-11e7-a349-00163efdd8db/chat-stats/daily/'
                         '?start_date={}'
                         '&end_date={}'.format(start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")),
                         headers={
                             'Authorization': 'Token '+auth_token
                         })
        if r.status_code == 401:
            return HttpResponseBadRequest('Unauthorized')

        # Save this request-response to cache
        stats = r.json()
        cache.set(cache_key, json.dumps(stats), timeout=None)  # Infinite expiration time

    # Sort, paginate, and return daily numbers as JSON
    stats_by_date = sorted(stats['by_date'], key=lambda x: datetime.strptime(x['date'], "%Y-%m-%d"))
    is_paginated = len(stats_by_date) > 5
    return JsonResponse({
        'by_date': list(map(
            lambda daily_stats: dict(
                conversation_count=daily_stats['conversation_count'],
                missed_chat_count=daily_stats['missed_chat_count'],
                visitors_with_conversation_count=daily_stats['visitors_with_conversation_count'],
                date=daily_stats['date']
            ),
            stats_by_date[(page-1)*5:(page-1)*5+5] if is_paginated else stats_by_date
        )),
        'paginated': is_paginated,
        'current_page': page,
        'max_page': math.ceil(len(stats_by_date)/5)
    })
