from typing import Any
from django.db.models.query import QuerySet
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from .models import Question, Choice
from django.template import loader
from django.views import generic


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # template = loader.get_template('polls/index.html')
    # context = {"latest_question_list" : latest_question_list}
    # return HttpResponse(template.render(context, request))
    context = {"latest_question_list" : latest_question_list}
    return render(request, "polls/index.html", context)

def detail(request, question_id):
    # try:
    #     question = Question.objects.get(pk = question_id)
    # except Question.DoesNotExist:
    #     raise Http404("Question does not exist")
    # # return HttpResponse("You're looking at question %s." % question_id)
    # return render(request, "polls/detail.html", {"question" : question})
    question = get_object_or_404(Question, pk = question_id)
    return render(request, "polls/detail.html", {"question" : question})

def results(request, question_id):
    question = get_object_or_404(Question, pk = question_id)
    return render(request, "polls/results.html", {"question" : question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk = question_id)
    try:
        seleted_choice = question.choice_set.get(pk = request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, "polls/detail.html",
                     {"question" : question},
                     {"error_message" : "You didn't select a choice.", })
    else:
        seleted_choice.votes += 1
        seleted_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
    
class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"
    
    def get_queryset(self) -> QuerySet[Any]:
        return Question.objects.order_by("-pub_date")[:5]
    
class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"
    
class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"
