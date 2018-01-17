# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, render
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.views import login
from datetime import datetime
from .models import Question, Plan, Event
from pytz import utc


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


def vote(request, question_id):
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
    if request.user.is_authenticated:
        print(request.user.get_full_name())
        # {'username':request.user.username})
        return render(request, 'polls/user_profile.html', )
    else:
        return render(request, 'polls/user_profile.html', {'error_message': "Musisz być zalogowany!"})


def event(request):
    if request.method == "POST":

        try:
            start_date = request.POST['start_date']
            start_time = request.POST['start_time']
            duration = request.POST['duration']
            title = request.POST['title']
            start_datetime = utc.localize(datetime.combine(
                datetime.strptime(start_date, "%Y-%m-%d"),
                datetime.strptime(start_time, "%H:%M").time()))
            durationTZ = datetime.strptime(duration, "%H:%M").time()
            quantity = request.POST['quantity']
            print(durationTZ, duration)
            new_event = Event.objects.create(
                searching_start_time=start_datetime,
                duration=durationTZ,
                title=title,
                quantity=quantity
            )

            message = {
                'mtype': "success",
                'text': "Pomyślnie dodano do bazy danych",
                'bold': "Sukces!"
            }

            return render(request, 'polls/create_event.html', {'message': message})
        except:
            message = {
                'mtype': "danger",
                'text': "Nie udało się dodać planów do bazy danych",
                'bold': "Błąd!"
            }

            return render(request, 'polls/create_event.html', {'message': message})
    else:
        return render(request, 'polls/create_event.html')


def plans(request):
    if request.method == "POST":
        try:
            start_date = request.POST['start_date']
            start_time = request.POST['start_time']
            end_date = request.POST['end_date']
            end_time = request.POST['end_time']
            title = request.POST['title']
            start_datetime = utc.localize(datetime.combine(
                datetime.strptime(start_date, "%Y-%m-%d"),
                datetime.strptime(start_time, "%H:%M").time()))
            end_datetime = utc.localize(datetime.combine(
                datetime.strptime(end_date, "%Y-%m-%d"),
                datetime.strptime(end_time, "%H:%M").time()))

            new_plan = Plan.objects.create(
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
        except:
            message = {
                'mtype': "danger",
                'text': "Nie udało się dodać planów do bazy danych",
                'bold': "Błąd!"
            }

            return render(request, 'polls/add_plans.html', {'message': message})
    else:
        return render(request, 'polls/add_plans.html')
