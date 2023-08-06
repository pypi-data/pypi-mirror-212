from django.shortcuts import get_object_or_404

def fetch_object_or_404(model, url_kwarg, var_name):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            id_ = kwargs.get(url_kwarg)
            obj = get_object_or_404(model, pk=id_)
            kwargs[var_name] = obj
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
