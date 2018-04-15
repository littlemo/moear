
def version(request):
    """
    返回用于渲染模板的版本号上下文变量 ``version``
    """
    try:
        from server.config import version as ver
        ver_name = ver.version_name
    except ImportError:
        ver_name = 'Unknown'
    return {
        'version': ver_name,
    }
