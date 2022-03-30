from django.core.exceptions import ValidationError

 
####################################################################################################
# Save images
####################################################################################################

def validate_size_image(file_obj):
    """ Проверка размера файла
    """
    magabyte_limit = 4
    if file_obj.size > magabyte_limit * 1024 * 1024:
        raise ValidationError(f"Максимальный размер файла {magabyte_limit}MB")
    

def get_path_upload_avatar(instance, file):
    """ Построение пути к файлу, format: (media)/avatar/user_id/photo.jpg
    """
    return f'avatar/{instance.id}/{file}'

def get_path_upload_post_image(instance, file):
    """ Построение пути к файлу, format: (media)/post/post_id/photo.jpg
    """
    print(instance.__dict__.keys())
    return f'post/{instance.PostID_id}/{file}'

def get_path_upload_post_link_image(instance, file):
    """ Построение пути к файлу, format: (media)/post/post_id/links/photo.jpg
    """
    return f'post/{instance.PostID_id}/links/{file}'


 
####################################################################################################
# All work with IP
####################################################################################################

PRIVATE_IPS_PREFIX = ('10.', '172.', '192.', )

def get_client_ip(request):
    """ Памятка
        How does get_ip() work?

        If nginx is a reverse proxy and gunicorn is the app server, 
        it's always getting requests from nginx on the local machine.

        The real ip that nginx sends to the app server is in my case HTTP_X_REAL_IP via 
        the nginx conf line proxy_set_header X-Real-IP $remote_addr;

        So you might want to set that, and in your django app account 
        for the different header 
        by either using your new IP header 
        or set request.META['REMOTE_ADDR'] = request.META['HTTP_X_REAL_IP']
    """

    """get the client ip from the request
    """
    remote_address = request.META.get('REMOTE_ADDR')
    # set the default value of the ip to be the REMOTE_ADDR if available
    # else None
    ip = remote_address
    # try to get the first non-proxy ip (not a private ip) from the
    # HTTP_X_FORWARDED_FOR
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        proxies = x_forwarded_for.split(',')
        # remove the private ips from the beginning
        while (len(proxies) > 0 and
                proxies[0].startswith(PRIVATE_IPS_PREFIX)):
            proxies.pop(0)
        # take the first ip which is not a private one (of a proxy)
        if len(proxies) > 0:
            ip = proxies[0]
    return ip



