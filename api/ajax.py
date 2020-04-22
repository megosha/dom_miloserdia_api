import json
import os
from datetime import datetime
import environ

from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from django.conf import settings
from front import models


@method_decorator(csrf_exempt, name='dispatch')
class Feedback(View):
    def resp(self, status: bool = True, msg: str = 'OK'):
        key = 'response' if status else 'error'
        return HttpResponse(json.dumps({key: msg}))
    def post(self, request):
        try:
            form = dict(json.loads(request.body)["form"]['data'])
            phone = form['phone']
            email = form.get('email')
            name = form['name']
            message = form['message']
        except Exception as e:
            return  self.resp(False, f'Ошибка отправки сообщения: {e}')
        subject = 'Новое обращение через форму обратной связи "Дом Милосердие"'
        message = f'ФИО: {name} \nТелефон: {phone}\nПочта: {email}\nСообщение: "{message}"'
        base_dir = settings.BASE_DIR
        env = environ.Env()
        env.read_env(os.path.join(base_dir, '.env'))
        from_email = env('FROM_EMAIL')
        sets = models.Settings.objects.get()
        emails = sets.mailto
        filename = os.path.join('/tmp', 'dom_miloserdia_rita', 'logs', 'feedback_log.txt')
        try:
            send_mail(subject, message, from_email, emails)
        except Exception as e:
            print(e)
            try:
                with open(filename, 'a', encoding='utf-8') as inp:
                    inp.write(
                        str(datetime.now()) + str(form) + str(e) + "\n")
            except Exception as err:
                print(err)
            return JsonResponse({"error": "1"})
        try:
            with open(filename, 'a', encoding='utf-8') as inp:
                inp.write(
                    str(datetime.now()) + str(form) + "\n")
        except Exception as err:
            print(err)
        return self.resp()