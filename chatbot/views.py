from django.shortcuts import render, HttpResponse, render
from .forms import InputForm
from openai._client import OpenAI
from django.conf import settings
from dotenv import load_dotenv
import textwrap
import os
import google.generativeai as genai
from IPython.display import Markdown

# Create your views here.

def home(request):
    return render(request, "chatbot/home.html")

def about(request):
    return render(request, "chatbot/about.html")


load_dotenv()
client = OpenAI(api_key=settings.OPENAI_API_KEY)

def generate_message(system_input, user_input):
    message = [{
        'role':'system',
        'content':system_input},
        {'role':'user',
         'content':user_input
    }]
    return message

def generate_response(system_input, user_input, model='gpt-3.5-turbo', temperature = 0.2):
    
    messages = generate_message(system_input, user_input)

    response = client.chat.completions.create(model=model,
                                 messages = messages,
                                 temperature = temperature)
    
    return response.choices[0].message.content

def openai_bot(request):    
    response_text = None

    if request.method == 'POST':
        form = InputForm(request.POST)
        if form.is_valid():
            user_input = form.cleaned_data['user_input']
            print("user_input",user_input)
            system_input = "You are a generalist who is expert in all the fields.Respond to user input to the best of your ability. You should sound friendly.\
                with every question user ask, chellange them to ask more tougher question and reply in short and crisp answer.\
                    If you do not know the answer, than say sorry in a funny way like you do not mean it and it's okay to not know some of the things.\
                        At the end, ask user if they need more assistance."


            response_text = generate_response(system_input, user_input)
            
    else:
        form = InputForm()

    return render(request, 'chatbot/openai.html', {'form': form, 'response': response_text})



# generating google gemini response
GOOGLE_API_KEY = settings.GOOGLE_API_KEY

def to_markdown(text):
    text = text.replace('*', ' *')
    return Markdown(textwrap.indent(text,'>', predicate=lambda _:True))


genai.configure(api_key=GOOGLE_API_KEY)



def get_resposne_google(user_input):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(user_input)
    return (response.text)

def gemini_bot(request):

    resposnse_text = None

    if request.method == "POST":
        form = InputForm(request.POST)
        if form.is_valid():
            user_input = form.cleaned_data['user_input']
            print("user_input",user_input)

            resposnse_text = get_resposne_google(user_input)

    else:
        form = InputForm()

    return render(request, "chatbot/gemini.html", {'form': form, 'response': resposnse_text})




def input_view(request):
    user_input = ''
    if request.method == 'POST':
        form = InputForm(request.POST)
        if form.is_valid():
            user_input = form.cleaned_data['user_input']
            form = InputForm() 
    else:
        form = InputForm()

    return render(request, 'chatbot/input.html', {'form': form, 'user_input': user_input})
