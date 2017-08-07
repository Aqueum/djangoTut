# djangoTut setup

## Setup vagrant box
- Pick box from [Vagrant](https://app.vagrantup.com/boxes/)
- I chose [ubuntu/xenial64](https://app.vagrantup.com/ubuntu/boxes/xenial64)
  - create new folder, I called mine `djangoTut`
  - I added the path to djangoTut as an alias called djangoTut by:
    - nano .bash_profile
    - add the line: `alias djangoTut='cd "/Users/PATH_TO_YOUR_DJANGOTUT_FOLDER"'
  - navigate to new folder in terminal
  - `vagrant init ubuntu/xenial64`
  - edit vagrant file
    - uncomment `# config.vm.network "forwarded_port", guest: 80, host: 8080, host_ip: "127.0.0.1"
`
    - change ports `80` and `8080` to `8000` as that's what the django development server uses
    - so you now have `config.vm.network "forwarded_port", guest: 8000, host: 8000, host_ip: "127.0.0.1`
  - `vagrant up` if first time or `vagrant reload` to load the new vagrant file
  - `vagrant box update` to get latest version
  - `vagrant ssh` to SSH into your new box
  
## Install Django
- `python3 -m django --version` to confirm no django installed (or check version)
  - [remove django](https://docs.djangoproject.com/en/1.11/topics/install/#removing-old-versions-of-django) if you have an out of date version
- [install database](https://docs.djangoproject.com/en/1.11/topics/install/#database-installation), if not SQLite, but tutorial uses SQLite
- install pip
  - `sudo apt-get update --fix-missing` 
  - `sudo apt install python3-pip` to install pip
  - `pip3 install --upgrade pip` to upgrade pip
- setup [virtualenv](https://virtualenv.pypa.io/en/stable/)
  - `sudo pip3 install virtualenv` to install virtualenv
  - `cd /vagrant`
  - `virtualenv ENV` to create a new virtual environment in directory ENV
  - `source ENV/bin/activate` to activate virtual env
- `pip install Django` to install Django
- `python -m django --version` to check installed version - I have 1.11.4
  
## Set up Django project
- `django-admin startproject mysite` to create django settings, database configuration & file structure
- check project working
  - `cd /vagrant/mysite`
  - `python manage.py runserver 0.0.0.0:8000` to run lightweight **non-production** development server - [here's why 0.0.0.0.:8000](https://stackoverflow.com/questions/33129651/access-web-server-on-virtualbox-vagrant-machine-from-host-browser)
  - Check 'It worked!' at [localhost:8000](http://localhost:8000/)
  
## Create app
- ctrl-c to exit server
- `cd /vagrant/mysite` to get to folder with manage.py
- `python manage.py startapp polls` to create polls app starter

## Add a view
- edit `polls/views.py` to: 
```
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
```
- add new polls/urls.py with content: 
```
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
]
```  
- add url pattern `url(r'^polls/', include('polls.urls')),` and `from django.conf.urls import include` to mysite/urls.py so we have:
```
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^polls/', include('polls.urls')),
    url(r'^admin/', admin.site.urls),
]
```
- check it works:
  - `python manage.py runserver 0:8000`
  - browse `http://127.0.0.1:8000/polls/`
- url() takes for arguments: regex, view, kwargs & name - see [docs](https://docs.djangoproject.com/en/1.11/ref/urls/#url) and foot of [tutorial page](https://docs.djangoproject.com/en/1.11/intro/tutorial01/)

## Set up database
- If not SQLite see [databases](https://docs.djangoproject.com/en/1.11/ref/settings/#std:setting-DATABASES), ensure database set up with `CREATE DATABASE database_name;` in database interactive prompt, and that the user given to `mysite/settings.py` has create database privelages.
- change `mysite/settings.py` to have `LANGUAGE_CODE = 'en-gb'` and `TIME_ZONE = 'Europe/London'`
- in terminal `cd /vagrant/mysite` & `source ../ENV/bin/activate`
- `python manage.py migrate` to create tables for INSTALLED_APPS

## Create models
- Edit `polls/models.py` to:
```
from django.db import models


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
      return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
      return self.choice_text
```

## Activate models
- add `'polls.apps.PollsConfig',` to top of `INSTALLED_APPS`. list in `mysite/settings.py`
- `python manage.py makemigrations polls` to create migrations for model changes
- optional `python manage.py sqlmigrate polls 0001` to see what SQL Django thinks is needed
- optional `python manage.py check` to check for project problems
- `python manage.py migrate` to create model tables in database

## - Optional, play with API
- `python manage.py shell` to invoke Python shell with env variable & import bath
- `from polls.models import Question, Choice` to import model classes
- `Question.objects.all()` to check no questions
- `from django.utils import timezone`
- `q = Question(question_text="What's new?", pub_date=timezone.now())` to create new question
- `q.save()` to save question
- `q.id` to get question ID (1 in this case)
- `q.question_text` to get question text ("What's new?" in this case)
- `q.pub_date` to get question timestamp (datetime.datetime(2017, 8, 3, 10, 18, 23, 238260, tzinfo=<UTC>) in this case)
- `q.question_text = "What's up?"` change question
- `q.save()` to save question
- `Question.objects.all()` to get all questions
- `Question.objects.filter(id=1)` or `Question.objects.get(pk=1)` to get first question
- `Question.objects.filter(question_text__startswith='What')` to filter by start text
- `from django.utils import timezone`
- `current_year = timezone.now().year`
- `Question.objects.get(pub_date__year=current_year)` to get this year's questions
- `q = Question.objects.get(pk=1)`
- `q.choice_set.all()` display choices (none to date)
- `q.choice_set.create(choice_text='Not much', votes=0)` create a choice
- `q.choice_set.create(choice_text='The sky', votes=0)` create another choice
- `c = q.choice_set.create(choice_text='Just hacking again', votes=0)`
- `c.question` show choice objects have access to related question objects
- `q.choice_set.all()` and vice versa
- `q.choice_set.count()` to get number of choices (currently 3)
- `Choice.objects.filter(question__pub_date__year=current_year)` use __ to separate relationships
- `c = q.choice_set.filter(choice_text__startswith='Just hacking')`
- `c.delete()` to dete a choice
- see [Accessing related objects](https://docs.djangoproject.com/en/1.11/ref/models/relations/), [Field lookups](https://docs.djangoproject.com/en/1.11/topics/db/queries/#field-lookups-intro) & [Database API reference](https://docs.djangoproject.com/en/1.11/topics/db/queries/)

## Create Admin User & log in
- `python manage.py createsuperuser`
- enter username, email address & passwordx2 (see password manager 'django scratch')
- `python manage.py runserver 0:8000` to run server
- [localhost:8000/admin](http://localhost:8000/admin)
- & log in with previously saved credentials
- edit `polls/admin.py` to:
```
from django.contrib import admin

from .models import Question

admin.site.register(Question)
```

## Create views
- edit `polls/views.py` to:
```
from django.http import HttpResponse

from .models import Question


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    output = ', '.join([q.question_text for q in latest_question_list])
    return HttpResponse(output)


def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)


def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
```
- wire up the views in `polls/urls.py` to give:
```
from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /polls/
    url(r'^$', views.index, name='index'),
    # ex: /polls/5/
    url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
    # ex: /polls/5/results/
    url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
    # ex: /polls/5/vote/
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
]
```
### Add templates
- create file `/polls/templates/polls/index.html` with content:
```
{% if latest_question_list %}
<ul>
    {% for question in latest_question_list %}
    <li><a href="{% url 'detail' question.id %}">{{ question.question_text }}</a></li>
    {% endfor %}
</ul>
{% else %}
<p>No polls are available.</p>
{% endif %}
```
- create file `/polls/templates/polls/detail.html` with content:
```
<h1>{{ question.question_text }}</h1>
<ul>
{% for choice in question.choice_set.all %}
    <li>{{ choice.choice_text }}</li>
{% endfor %}
</ul>
```
- update `polls/views.py` to:
```
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from .models import Question


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
```
(after this bit I started step by step again)

## Write a simple form
- change `polls/templates/polls/detail.html` to:
```
<h1>{{ question.question_text }}</h1>

{% if error_message %}<p><strong>{{ error_message }}</strong></p>{% endif %}

<form action="{% url 'polls:vote' question.id %}" method="post">
{% csrf_token %}
{% for choice in question.choice_set.all %}
    <input type="radio" name="choice" id="choice{{ forloop.counter }}" value="{{ choice.id }}" />
    <label for="choice{{ forloop.counter }}">{{ choice.choice_text }}</label><br />
{% endfor %}
<input type="submit" value="Vote" />
</form>
```

## Add votecounting
- change `polls/views.py` to:
```
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Question, Choice


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


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
```
- and change the results clause to:
```
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})
```
- add a results template:
```
<h1>{{ question.question_text }}</h1>

<ul>
{% for choice in question.choice_set.all %}
    <li>{{ choice.choice_text }} -- {{ choice.votes }} vote{{ choice.votes|pluralize }}</li>
{% endfor %}
</ul>

<a href="{% url 'polls:detail' question.id %}">Vote again?</a>
```

# Add generic views
- change `polls/urls.py` to:
```
from django.conf.urls import url

from . import views

app_name = 'polls'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
]
```
- Amend `polls/views.py` to:
```
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from .models import Choice, Question


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'
```
leaving `def vote`... as previous

## Testing
- add bug to `polls/models.py` with:
```
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
```
- add test code to `polls/tests.py`:
```
import datetime

from django.utils import timezone
from django.test import TestCase

from .models import Question


class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)
```
- run test code with `python manage.py test polls`
- fix bug in `polls/models.py` with:
```
def was_published_recently(self):
    now = timezone.now()
    return now - datetime.timedelta(days=1) <= self.pub_date <= now
```
- add more test code to `polls/tests.py`:
```
def test_was_published_recently_with_old_question(self):
    """
    was_published_recently() returns False for questions whose pub_date
    is older than 1 day.
    """
    time = timezone.now() - datetime.timedelta(days=1, seconds=1)
    old_question = Question(pub_date=time)
    self.assertIs(old_question.was_published_recently(), False)

def test_was_published_recently_with_recent_question(self):
    """
    was_published_recently() returns True for questions whose pub_date
    is within the last day.
    """
    time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
    recent_question = Question(pub_date=time)
    self.assertIs(recent_question.was_published_recently(), True)
```
- add `from django.utils import timezone` to `polls/views.py` and change its get_queryset to:
```
    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]
```
- add the following to `polls/tests.py`:
```
from django.urls import reverse


def create_question(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        create_question(question_text="Past question 1.", days=-30)
        create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )
```
- add exclusion to DetailView in `polls/views.py`:
```
def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())
```
- add tests in `polls/tests.py`:
```
class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question(question_text='Future question.', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(question_text='Past Question.', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
```

## Look and feel
- add directory `polls/static/polls`
- add file `styles.css` with content:
```
li a {
    color: green;
}
```
- add link in `polls/templates/polls/index.html`:
```
{% load static %}

<link rel="stylesheet" type="text/css" href="{% static 'polls/style.css' %}" />
```
- add directory `polls/static/polls/images`
- add file `python.gif`
- add block to `style.css`:
```
body {
  background: white url("images/python.gif") no-repeat right bottom;
}
```

## Customise admin functionality
- change `polls/admin.py` to:
```
from django.contrib import admin

from .models import Question
from .models import Choice


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 0


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date']}),
    ]
    inlines = [ChoiceInline]


admin.site.register(Question, QuestionAdmin)
```
- add questions list columns to `polls/admin.py`:
```
    list_display = ('question_text', 'pub_date', 'was_published_recently')

```
- expand was_published_recently in `polls/models.py`:
```
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'
```
-  add `list_filter = ['pub_date']` to `polls/admin.py`'s QuestionAdmin class to give filter sidebar
-  add `search_fields = ['question_text']` to `polls/admin.py`'s QuestionAdmin class to give search box

## Customise admin appearance
- note we'd normally use [django.contrib.admin.AdminSite.site_header](https://docs.djangoproject.com/en/1.11/ref/contrib/admin/#django.contrib.admin.AdminSite.site_header) rather than overriding the template
- add `mysite/templates/admin` (top level mysite - containing manage.py)
- edit `DIRS` in `mysite/mysite/settings.py` to `'DIRS': [os.path.join(BASE_DIR, 'templates')],`
- add `/Users/Shared/Dropbox/P - Education/Martin - Education/Programming/djangoTut/ENV/lib/python3.5/site-packages/django/contrib/admin/templates/admin/base_site.html` to `mysite/templates/admin`
- edit `base_site.html` to:
```
{% extends "admin/base.html" %} {% block title %}{{ title }} | {{ site_title|default:_('Django site admin') }}{% endblock%}
{% block branding %}
<h1 id="site-name"><a href="{% url 'admin:index' %}">Polls Administration</a></h1>
{% endblock %}
```

## Package for reuse
- check [pip](https://pypi.python.org/pypi/pip) & [setuptools](https://pypi.python.org/pypi/setuptools) installed
- move `polls` to new dir `django-polls`
- add `django-polls/README.rst` with content:
```
=====
Polls
=====

Polls is a simple Django app to conduct Web-based polls. For each
question, visitors can choose between a fixed number of answers.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "polls" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'polls',
    ]

2. Include the polls URLconf in your project urls.py like this::

    url(r'^polls/', include('polls.urls')),

3. Run `python manage.py migrate` to create the polls models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a poll (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/polls/ to participate in the poll.
```
- Add `django-polls/LICENSE` file
- Add `django-polls/setup.py` file with content:
```
import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-polls',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    license='BSD License',  # example license
    description='A simple Django app to conduct Web-based polls.',
    long_description=README,
    url='https://www.example.com/',
    author='Your Name',
    author_email='yourname@example.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: X.Y',  # replace "X.Y" as appropriate
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',  # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        # Replace these appropriately if you are stuck on Python 2.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
```
- Add `django-polls/MANIFEST.in` which includes all non python module & package files:
```
include LICENSE
include README.rst
recursive-include polls/static *
recursive-include polls/templates *
recursive-include docs *
``` 
- Add documentation folder `django-polls/docs` and populate
- navigate to within `django-polls` and run `python setup.py sdist`

## Install as user library
- cd /vagrant
- `pip install --user django-polls/dist/django-polls-0.1.tar.gz` is what they say, but in a virtual env I could only manage `pip install django-polls/dist/django-polls-0.1.tar.gz`
- I don't know why the above failed and don't have time now to investigate, so I just copied polls back in to the base mysite


# To launch
- in terminal `djangoTut` or navigate to the folder with your vm
- `./rds1` (a bash script I set up to do the following)
  - `vagrant up`
  - `vagrant ssh`
- `/vagrant/rds2` (a bash script I set up to do the following)
  - `cd /vagrant/mysite`
  - `source ../ENV/bin/activate`
  - `python manage.py runserver 0:8000`
- [localhost:8000/polls](http://localhost:8000/polls)