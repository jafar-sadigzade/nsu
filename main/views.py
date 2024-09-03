from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404

from main.forms import CommentForm, NewsSearchForm, ContactForm
from main.models import HomePage, New, Comment, Event, Staff


def index(request):
    banners = HomePage.objects.all()
    events = Event.objects.all()
    teachers = Staff.objects.filter(position='Müəllim')
    context = {
        "banners": banners,
        "events": events,
        "teachers": teachers,
    }
    return render(request, "index.html", context)


def news_request(request):
    return render(request, "news.html")


def news_details(request, news_id):
    news = get_object_or_404(New, id=news_id)

    latest_news = get_list_or_404(New.objects.filter(status='published').order_by('-date'))[0:3]

    previous_news = New.objects.filter(id__lt=news_id).order_by('-id').first()
    next_news = New.objects.filter(id__gt=news_id).order_by('id').first()

    search_form = NewsSearchForm(request.GET)
    if search_form.is_valid():
        query = search_form.cleaned_data.get('query')
        if query:
            search_results = New.objects.filter(
                Q(title__icontains=query) | Q(content__icontains=query)
            ).distinct()
        else:
            search_results = None
    else:
        search_results = None

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.news = news
            comment.user = request.user
            comment.save()
            messages.success(request, 'Sizin rəyiniz uğurla əlavə edildi!')
            return redirect('news_detail', news_id=news.id)
    else:
        form = CommentForm()

    context = {
        "news": news,
        "latest_news": latest_news,
        "previous_news": previous_news,
        "next_news": next_news,
        "form": form,
        "total_comments": Comment.objects.filter(news=news).count(),
        "comments": Comment.objects.filter(news=news),
        "search_form": search_form,
        "search_results": search_results,
    }
    return render(request, "news-details.html", context)


def events_request(request):
    events = Event.objects.all()
    return render(request, "events.html", {"events": events})


def event_details(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, "event-details.html", {"event": event})


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Müraciətiniz qeydə alındı!")
            return redirect('contact')
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})
