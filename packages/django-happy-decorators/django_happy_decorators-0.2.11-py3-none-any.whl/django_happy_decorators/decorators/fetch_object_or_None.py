

def fetch_object_or_None(model, url_kwarg, var_name):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            id_ = kwargs.get(url_kwarg)
            obj = model.objects.filter(pk=id_).first()
            kwargs[var_name] = obj
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
