from ast import arg
from multiprocessing import context
from django.shortcuts import render, redirect
from django.http import HttpResponse

#from mysite.polls.forms import QuestionForm
from .models import Question, Choice
from django.template import loader
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import ListView
from .forms import QuestionForm

# Create your views here.

#def index(request):
#    questions = Question.objects.all()
#    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    #output = ', '.join([q.question_text for q in latest_question_list])
    #return HttpResponse(output)
#    template = loader.get_template('polls/index.html')
#    context = {
#        'mensaje': "Lista de encuestas",
#        'latest_question_list': latest_question_list,
#    }
#    return HttpResponse(template.render(context, request))

class IndexView(ListView): 
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(*kwargs)
        context ['mensaje'] = "Lista de encuestas"
        return context


    def get_queryset(self):
        query = Question.objects.order_by('-pub_date')[:5]

        return query


def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    context = {
        'mensaje': "Detalle de la encuestas",
        'question': question,
    }
    return render(request, 'polls/detail.html', context)
    #return HttpResponse("You're looking at question %s." % question_id)

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    print("hola")
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
        print("guardaste el voto")
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def add_or_change_question(request, question_id=None):
    question = None
    #idea = None
    if question_id:
        question = get_object_or_404(Question, pk=question_id)
        #idea = get_object_or_404(Question, pk=pk)
        if request.method == "POST":
            form = QuestionForm(
            data=request.POST,
            files=request.FILES,
            instance=question
            )
            if form.is_valid():
                question = form.save()
                return HttpResponseRedirect(reverse('polls:detail', args=(question.id,)))
               # return redirect("polls:detail", pk=question.pk)
        else:
            form = QuestionForm(instance=question)
    context = {"question": question, "form": form}
    return render(request, "polls/polls_form.html", context)

