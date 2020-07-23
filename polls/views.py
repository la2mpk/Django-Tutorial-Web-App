from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from .models import Question, Choice


class IndexPageView(generic.ListView):
    model = Question
    template_name = 'polls/index.html'
    context_object_name = 'latest_questions_list'

    def get_queryset(self):
        queryset = Question.objects.filter(pub_date__lte=timezone.now())
        queryset = queryset.order_by('-pub_date')[:5]
        return queryset


class DetailPageView(generic.DetailView):
    model = Question
    template_name = 'polls/details.html'
    context_object_name = 'question'

    def get_queryset(self):
        queryset = Question.objects.filter(pub_date__lte=timezone.now())
        return queryset


class ResultsPageView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'
    context_object_name = 'question'

    def get_queryset(self):
        queryset = Question.objects.filter(pub_date__lte=timezone.now())
        return queryset


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        error_message = 'You didn\'t select a choice'
        context = {'question': question, 'error_message': error_message}
        return render(request, 'polls/details.html', context)
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id, )))
