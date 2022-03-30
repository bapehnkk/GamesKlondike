from django.shortcuts import render
from django.utils import timezone
from django.db.models import Q


from src.posts.models import PostGame

def home(request):
    """ Home/Index page
    """
    if request.GET:
        search = request.GET.get('search')
    else:
        search = ''

    dict = {
        'header': get_header_content(request),
        'cards': get_cards(search),
    }
    return render(request, 'front/home.html', dict)


try:
    """ Этот try для моментов когда удаляется DB и нужно сделать новые миграции
        Берётся первая запись из бд. 
        Если бд нет, то невозможно применить миграции. =)
    """
    def post(request, game=PostGame.objects.all()[0].id):
        dict = get_post_by_id(game)
        return render(request, 'front/post.html', dict)
except:
    """ На релизе удалить, или как-то пофиксить. =)
    """
    def post(request, game=0):
        dict = get_post_by_id(game)
        return render(request, 'front/post.html', dict)





def more_cards(request, post_count=0):
    dict = {
        'cards': get_cards(post_count=post_count),
    }
    return render(request, 'card.html', dict)


def get_cards(selector='', order_by='Title', post_count=0) -> list:
    """ Взять все посты из БД и отдать в виде массива
    """
    # посты, по умолчанию 6 шт. и прибавляются по 6
    posts = PostGame.objects.filter(
        Q(Title__contains=selector) | Q(Description__contains=selector)).order_by(order_by)[post_count:post_count+6]
    cards = ([{
        'title': f'{post.Title} id:{post.id}',
        'images': (post.post_images.all()),
        'link': f'/post/{post.id}',
        'text': f'{post.Description}',
        'date': post.PubDate,
        'tags': ([{
                'link': f'/{tag}',
                'text': f'{tag}',
        } for tag in post.Tags.all()]),
    } for post in posts])

    return cards


def get_post_by_id(id: int) -> dict:
    """ Взять пост из БД 
    """
    post = PostGame.objects.get(id=id)
    post = {
        'title': f'{post.Title} id:{post.id}',
        'images': post.post_images.all(),
        'links': post.post_links.all(),
        'text': post.Description,

        'publisher': {
            'date': post.PubDate,
            'link': f'/user/{post.Email.id}',
            'user': post.Email.UserName, },

        'tags': ([{
            'link': f'/tag/{tag}',
            'text': tag,
        } for tag in post.Tags.all()]),

        'comments': ([{
            'text': comment.Text,
            'date': comment.PubDate,
            'user': comment.Email.UserName,
            'link': f'/user/{comment.Email.id}',
            'likes': f'{comment.like_dislike_comment.filter(Status=True).count()}',
            'dislikes': f'{comment.like_dislike_comment.filter(Status=False).count()}',
        } for comment in post.comment_post.all()])
    }
    return post


def get_header_content(request) -> dict:
    if request.session._session == {}:
        return {}

    header = {
        'alerts': get_alerts(),
        # 'playlists': []   # мб не надо, но когда-нибудь можно запилить
    }
    return header


def get_alerts() -> tuple:
    alerts = []
    for n in range(20):
        alerts.append({
            'image': 'img/no-image.png',
            'text': f'This is {n+1}\'s alert',
            'time': f'{timezone.now()}'
        })
    return tuple(alerts)

