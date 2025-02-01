import json

from django.http import QueryDict

from async_notifications.models import NewsLetter, NewsLetterTask, NewsLetterTemplate
from async_notifications.utils import get_basemodel_info
from async_notifications import settings as asettings
from markitup.markup import filter_func
from django.template import Context, Template
from async_notifications.models import NewsLetterTemplate
from django.core import mail
from .settings import SMTP_DEBUG
from django.conf import settings
import os

def render_template_newsletter(data):
    markup = filter_func(data)
    try:
        message = Template(markup)
        dev = message.render(Context({}))
    except Exception as e:
        dev = "Error ocurrido en: %s con el tipo <pre>%s</pre>"%(str(e), str(e.__class__.__name__))
    return dev

def get_template_name_from_path(path):
    return path.replace(asettings.TEMPLATES_NOTIFICATION, '')

def get_data(templateid, data):
    parent, extends = None, None
    if templateid:
        if isinstance(templateid, int):
            template=NewsLetterTemplate.objects.filter(pk=templateid).first()
        else:
            template=templateid
    return (data)



def get_form_data(obj):
    dev = QueryDict()
    if obj.recipient:
        dev = QueryDict(obj.recipient)
    return dev

def extract_template(obj,klass):
    form = klass.get_form(get_form_data(obj))
    klass.set_form(form)
    klass.get_queryset()
    return klass.get_emails_instance()

def get_subject_content(newsletter):
    message = Template(newsletter.subject)
    dev = message.render(Context({}))
    return dev

# Funcion creada por luis
'''def extract_separedcomma_emails(text):
    return text.split(', ')'''

#Funcion creada por mi para probar
def extract_separedcomma_emails(text):
    try:
        emails_list = json.loads(text)
        if isinstance(emails_list, list):
            return [email["value"] for email in emails_list if "value" in email]
    except json.JSONDecodeError:
        print("❌ Error: `newsletter.recipient` no es un JSON válido")
    return text.split(', ')

def get_newsletter_content(newsletter, useform=True):
    inst = get_basemodel_info(newsletter.template.model_base)
    klass = inst[2]()

    if useform:
        emailsiter = extract_template(newsletter, klass)
    else:
        emailsiter = extract_separedcomma_emails(newsletter.recipient)

    data = get_data(newsletter.template, newsletter.message)

    for email in emailsiter:

        template = render_template_newsletter(data)
        subject = get_subject_content(newsletter)

        yield email, template, subject


def get_connections_config():
    configs = asettings.NEWSLETTER_SEVER_CONFIGS or {}
    return configs


def get_from_email():
    configs = asettings.NEWSLETTER_SEVER_CONFIGS or {}
    if 'from' in configs:
        return configs['from']
    return settings.DEFAULT_FROM_EMAIL

def get_headers():
    headers= asettings.NEWSLETTER_HEADER or {}

    if headers == {}:
        return None
    return headers

def send_newsletter(newsletter):
    logs = {'exceptions': [], 'success': []}
    messages = []
    with mail.get_connection(**get_connections_config()) as connection:
        if SMTP_DEBUG:
            connection.connection.set_debuglevel(1)
        headers = get_headers()
        for email, messagetxt, subject in get_newsletter_content(newsletter, useform=False):
            print(f"Email antes de limpiar: {email}")
            # Esto lo acabo de agregar yo para ver si funciona
            if isinstance(email, dict) and "value" in email:
                email = email["value"]
            message = mail.EmailMessage(subject, messagetxt,
                                        get_from_email(),
                                        [email],
                                        connection=connection,
                                        headers=headers
                                        )
            message.content_subtype = "html"
            if newsletter.file:
                if os.path.isfile(settings.MEDIA_ROOT + newsletter.file.name):
                    message.attach_file(settings.MEDIA_ROOT + newsletter.file.name)
            messages.append(message)
        connection.fail_silently = True
        logs['total_sent'] = connection.send_messages(messages)
        print(f"Logs en sent_newsletter: {logs}")
    return logs


def task_send_newsletter_fnc(pk):
    newsletter = NewsLetter.objects.filter(pk=pk).first()
    logs={'total_sent': 0}
    if newsletter:
        logs = send_newsletter(newsletter)
        print(f"Logs en task_sent_newsletter_fnc() {logs}")
    return logs['total_sent']


def send_newsletter_task(pk):
    task = NewsLetterTask.object.filter(pk=pk).first()
    if task:
        newsletter = task.template
        send_newsletter(newsletter)