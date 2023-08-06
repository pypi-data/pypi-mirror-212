

from django.core.cache import cache
from django.http import HttpResponse
from django.shortcuts import redirect

def rate_limit(num_requests: int, 
               time_minutes: int, 
               redirect_url: str=None,
               mode='IP',
               error_message: str= "You have exceeded the maximum number of requests allowed."):
    """
        Decorator to limit the number of requests a user can make to a specific view within a given time frame.
            When the limit is reached, the user will be redirected to the specified redirect_url.

        :param num_requests: The number of requests allowed within the time frame.
        :type num_requests: int
        :param time_frame: The time frame, in seconds, in which the number of requests is limited.
        :type time_frame: int
        :param redirect_url: The URL to redirect the user to when the limit is reached.
        :type redirect_url: str
        :param mode: The mode to use for rate limiting. Can be 'IP' or 'USER' or "ALL".
        :type mode: str
        
        :return: The decorated view function.
        :rtype: function
    """
    
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            
            ip_address = request.META['REMOTE_ADDR']
            user = request.user
            
            if mode.lower() == 'ip':
                key = ip_address
            elif mode.lower() == 'user':
                key = user.id
            elif mode.lower() == 'all':
                key = 'all_visitors_key'     # This is a special case for rate limiting all users, regardless of IP address or user ID.
            else:
                raise ValueError('Invalid mode for rate limiting. Must be "IP" or "USER" [case insensitive].')
            
            requests = cache.get(key)
            if requests:
                if requests >= num_requests:
                    if redirect_url:
                        # redirect with a 429 status code
                        red = redirect(redirect_url)
                        # red.status_code = 429
                        return red
                    else:
                        res = HttpResponse(error_message)
                        res.status_code = 429
                        return res
                else:
                    cache.set(key, requests+1, time_minutes*60)
            else:
                cache.set(key, 1, time_minutes*60)

            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
