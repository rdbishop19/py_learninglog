from django.shortcuts import render

from .models import Topic

# Create your views here.
def index(request):
    """The home page for Learning Log"""
    return render(request, 'learning_logs/index.html')

def topics(request):
    """Show all topics."""
    topics = Topic.objects.order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)

def topic(request, topic_id):
    """Show a single topic and all its entries."""
    # Get topic
    topic = Topic.objects.get(id=topic_id)
    # Get all entries for that topic
    entries = topic.entry_set.order_by('-date_added') #'-': reverse sort
    context = {'topic': topic, 'entries': entries}
    # return page
    return render(request, 'learning_logs/topic.html', context)