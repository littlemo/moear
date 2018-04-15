
def version(request):
    """
    返回用于渲染模板的版本号上下文变量 ``version``
    """
    return {
        'version': 'v1.0.0',
    }
