from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
# from django.views.generic.edit import DeleteView

from .models import Topic, Entry
from .forms import TopicForm, EntryForm

# Create your views here.
def index(request):
    """The home page for Learning Log"""
    return render(request, 'learning_logs/index.html')

def check_topic_owner(topic, request):
    """Checks topic matches to its owner."""
    if topic.owner != request.user:
        raise Http404

@login_required
def topics(request):
    """Show all topics."""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
    """Show a single topic and all its entries."""
    # Get topic
    topic = Topic.objects.get(id=topic_id)
    check_topic_owner(topic, request)

    # Get all entries for that topic
    entries = topic.entry_set.order_by('-date_added') #'-': reverse sort
    context = {'topic': topic, 'entries': entries}
    # return page
    return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
    """Add a new topic."""
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = TopicForm()
    else:
        # POST data submitted; process data
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('learning_logs:topics'))

    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    """Add a new entry."""
    topic = Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = EntryForm()
    elif topic.owner == request.user:
        # POST data submitted; process data

        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('learning_logs:topic',
                                                args=[topic_id]))
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """Edit an existing entry."""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    check_topic_owner(topic, request)

    if request.method != 'POST':
        # Initial request; pre-fill form with the current entry.
        form = EntryForm(instance=entry)
    else:
        # POST data submitted; process data
        form = EntryForm(instance=entry, data=request.POST)
        request_name = request.POST.get('name')

        # TODO: add 'delete entry' method

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topic',
                                                args=[topic.id]))

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)

# TODO : add DELETE_ENTRY ability
# @login_required
# def entry_confirm_delete(request, entry_id):
#     entry = Entry.objects.get(id=entry_id)
#     entry.delete()

# class EntryDelete(DeleteView):
#     model = Entry
#     success_url = reverse_lazy('topic')