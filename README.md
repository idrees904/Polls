# Polls
API для системы опросов пользователей

#### Как развернуть  
```sh
git clone https://github.com/idrees904/Polls.git
cd Polls
python -m venv .env
.env\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py makemigrations api
python manage.py migrate
python manage.py createsuperuser --email admin@example.com --username admin
python manage.py runserver
```

#### Как получить все опросы или создать новый (GET, POST)
- http://127.0.0.1:8000/all_polls/

#### Как получить все вопросы или создать новый (GET, POST)
- http://127.0.0.1:8000/questions/

#### Как получить все ответы (GET)
- http://127.0.0.1:8000/answers/

#### Как получить все варианты ответов или создать новые (GET, POST)
- http://127.0.0.1:8000/answers_options/

#### Как получить активные опросы или создать новые (GET, POST)
- http://127.0.0.1:8000/active_polls/

#### Как получить пройденные пользователем опросы (GET)
- http://127.0.0.1:8000/complete_polls/

#### Как пройти опрос (POST)
- http://127.0.0.1:8000/polls/<poll_id>/questions/<question_id>

## Технологии
djangorestframework