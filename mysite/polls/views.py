from multiprocessing import context
from django.shortcuts import render
from django.http import HttpResponse
from .models import Question, Choice
from django.template import loader
from django.http import Http404

# Create your views here.

def index(request):
    questions = Question.objects.all()
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    #output = ', '.join([q.question_text for q in latest_question_list])
    #return HttpResponse(output)
    template = loader.get_template('polls/index.html')
    context = {
        'mensaje': "Lista de encuestas",
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))

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
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
