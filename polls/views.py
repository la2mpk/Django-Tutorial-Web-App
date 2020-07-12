from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.http import HttpResponse
from .models import Question


class IndexPageView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_questions_list'

    def get_queryset(self):
        queryset = Question.objects.order_by('-pub_date')[:5]
        return queryset


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'polls/details.html', context)


def results(request, question_id):
    return HttpResponse(f'You are looking at the results of question {question_id}')


def vote(request, question_id):
    return HttpResponse(f'You are voting on question {question_id}')
