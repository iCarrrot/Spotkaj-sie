# -*- coding: utf-8 -*-
"""Define views
"""

from datetime import datetime
from datetime import timedelta
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
import pytz
from .models import Question, Plan, Event, Choice
from .utils import find_term


def index(request):
    """
    View of main page
    """
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    """
    View of question detail
    """
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    """
    View of question result
    """
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


def vote(request, question_id):
    """
    Vote POST function
    """
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


def user_profile(request):
    """
    View of user profile
    """
    if request.user.is_authenticated:
        print(request.user.get_full_name())
        # {'username':request.user.username})
        return render(request, 'polls/user_profile.html', )
    return render(request,
                    'polls/user_profile.html',
                    {'error_message': "Musisz być zalogowany!"})


def event(request):
    """
    If GET - show event creating page.
    If POST - get data, find first available term,
    show page with proposed starting dates.
    """
    if request.method == "POST":

        try:
            start_date = request.POST['start_date']
            start_time = request.POST['start_time']
            duration = request.POST['duration']
            title = request.POST['title']
            eastern = pytz.timezone('Europe/Warsaw')
            start_datetime = eastern.localize(datetime.combine(
                datetime.strptime(start_date, "%Y-%m-%d"),
                datetime.strptime(start_time, "%H:%M").time()))
            duration = datetime.strptime(duration, "%H:%M")
            duration = timedelta(hours=duration.hour, minutes=duration.minute)
            quantity = request.POST['quantity']
            Event.objects.create(
                searching_start_time=start_datetime,
                duration=duration.total_seconds(),
                title=title,
                quantity=quantity
            )
            terms = Plan.objects.filter(end_time__gt=start_datetime)
            users = len(User.objects.filter())
            found_term = find_term(duration=int(duration.total_seconds() / 60),
                                   searching_start_time=start_datetime,
                                   terms=terms,
                                   quantity=int(quantity),
                                   users=users)
            (date, list_of_term) = found_term
            term_list = []
            for element in list_of_term:
                (start, end, _) = element
                time = start
                while duration + time < end:
                    term_list += [time]
                    time += timedelta(minutes=15)

            return render(request, 'polls/event_found.html', {'date': date,
                                                              'list_of_term': term_list,
                                                              'event': new_event})
        except Exception as ex:
            message = {
                'mtype': "danger",
                'text': "Nie udało się dodać planów do bazy danych",
                'bold': "Błąd!"
            }
            print(ex)
            return render(request, 'polls/create_event.html', {'message': message})
    else:
        return render(request, 'polls/create_event.html')


def plans(request):
    """
    If GET - show plans creating page.
    If POST - get data, create entry in database.
    """
    if request.method == "POST":
        try:
            start_date = request.POST['start_date']
            start_time = request.POST['start_time']
            end_date = request.POST['end_date']
            end_time = request.POST['end_time']
            title = request.POST['title']
            start_datetime = pytz.utc.localize(datetime.combine(
                datetime.strptime(start_date, "%Y-%m-%d"),
                datetime.strptime(start_time, "%H:%M").time()))
            end_datetime = pytz.utc.localize(datetime.combine(
                datetime.strptime(end_date, "%Y-%m-%d"),
                datetime.strptime(end_time, "%H:%M").time()))

            Plan.objects.create(
                user=request.user,
                start_time=start_datetime,
                end_time=end_datetime,
                title=title)
            message = {
                'mtype': "success",
                'text': "Pomyślnie dodano do bazy danych",
                'bold': "Sukces!"
            }

            return render(request, 'polls/add_plans.html', {'message': message})
        except Exception as ex:
            message = {
                'mtype': "danger",
                'text': "Nie udało się dodać planów do bazy danych",
                'bold': "Błąd!"
            }
            print(ex)
            return render(request, 'polls/add_plans.html', {'message': message})
    else:
        return render(request, 'polls/add_plans.html')


def delete_plans(request):
    """
    If user is superuser - delete all Plan entry
    """
    if request.method == "POST" and request.user.is_superuser:
        terms = Plan.objects.filter().delete()
        print(terms)
    return HttpResponseRedirect(reverse('polls:user_profile',))


def delete_events(request):
    """
    If user is superuser - delete all Event entry
    """
    if request.method == "POST" and request.user.is_superuser:
        terms = Event.objects.filter().delete
        print(terms)
    return HttpResponseRedirect(reverse('polls:user_profile',))


def new_event(request, event_id):
    """
    Add found date to created event
    """
    if request.method == "POST":
        event_object = get_object_or_404(Event, pk=event_id)
        start_time = request.POST['start_time']
        start_time = datetime.fromtimestamp(int(start_time[:-2]))
        event_object.found_time = start_time
        event_object.save()

    return HttpResponseRedirect(reverse('polls:user_profile',))
