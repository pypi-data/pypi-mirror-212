from django.http import HttpResponse

def if_not(parameter_name: str, 
               raise_error_code: int,
               error_message:str):
    """
        Decorator to check if the parameter is not set in the request or is False or is None. If it is, then raise an error. If not, then continue with the view.
        
        :param parameter_name: The name of the parameter to check.
        :param raise_error_code: The error code to raise if the parameter is not set.
        :error_message: The error message to display if the parameter is not set.
        :return: The decorated view function.
        :rtype: function
    """
    
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            # check if the request is a GET request
            parameter = None
            if request.method == 'GET':
                parameter = request.GET.get(parameter_name)
            elif request.method == 'POST':
                parameter = request.POST.get(parameter_name)
            elif request.method == 'PUT':
                parameter = request.PUT.get(parameter_name)
            elif request.method == 'DELETE':
                parameter = request.DELETE.get(parameter_name)
            else:
                raise ValueError('Invalid request method. Must be GET, POST, PUT, or DELETE.')
            
            if parameter is None or parameter == False:
                res = HttpResponse(error_message)
                res.status_code = raise_error_code
                return res

            else:
                return view_func(request, *args, **kwargs)
        return wrapper
    
    return decorator

