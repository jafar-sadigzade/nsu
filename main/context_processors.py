from main.models import New


def show_news(request):
    return {'news': New.objects.order_by('-date')}
