import datetime
import logging
import os
import sys

import requests
import vk_api
from django.conf import settings
from django.utils import timezone

from dom_miloserdia_api.celery import app
from front import models

# from PIL import Image
# from django.core.files import File

app.conf.task_default_queue = 'default'


@app.task(name='front.tasks.get_from_vk', ignore_result=True)
def get_from_vk():
    conf = models.Settings.objects.get()

    api = vk_api.VkApi(token=conf.vk_token).get_api()
    result = api.wall.get(domain=conf.vk_group, filter="owner")
    items = result.get('items')

    article_kind = models.ArticleKind.objects.get(pk=3)

    for item in items:
        article, new = models.Article.objects.get_or_create(
            vk_id=post_id,
            defaults={'date_publish': published, 'kind': article_kind}
        )


@app.task(name='front.tasks.update_lenta', ignore_result=True)
def update_lenta():
    try:
        tz = timezone.get_current_timezone()
        sett = models.Settings.objects.get()
        url = sett.rapidapi_url.format(iid=sett.instagram_id)
        headers = sett.rapidapi_header

        article_kind = models.ArticleKind.objects.get(pk=3)
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise Exception(f'StatusCode not 200: {response.status_code}, {response.text}')
        response_json = response.json()
        posts = response_json['edges']
        for i, post in enumerate(posts):
            post_id = post['node']['id']
            published = datetime.datetime.utcfromtimestamp(post['node']['taken_at_timestamp']).replace(tzinfo=tz)
            # article, new = models.Article.objects.get_or_create(instagram_id=post_id,
            #                                                     defaults={'date_publish': published})
            article, new = models.Article.objects.get_or_create(instagram_id=post_id,
                                                                defaults={'date_publish': published,
                                                                          'kind': article_kind})
            if new:
                if post['node']['edge_media_to_caption']['edges']:
                    text = post['node']['edge_media_to_caption']['edges'][0]['node']['text']
                    title = f"{text.split(' ')[0]} {text.split(' ')[1]} {text.split(' ')[2]} {text.split(' ')[3]}..."
                    text.replace('Реквизиты', '<a href="#reqv">Реквизиты</a>').replace('реквизиты',
                                                                                       '<a href="#reqv">реквизиты</a>')
                else:
                    text = ''
                    title = 'Фотоотчёт'

                # text += '\n\nИсточник: <a href="https://www.instagram.com/dommi_loserdie/">https://www.instagram.com/dommi_loserdie/</a>'
                # если пост - это одно видео или одна картинка
                if not 'edge_sidecar_to_children' in post['node']:
                    # если пост - это одно видео
                    # if post['node']['is_video']:
                    #     video_link = post['node']['video_url']
                    #     article.videolink = video_link

                    fname = f'{post["node"]["id"]}.jpg'
                    cover = os.path.join(settings.MEDIA_ROOT, 'images', 'covers', fname)
                    with open(cover, 'wb+') as dest:
                        preview = requests.get(post['node']['display_url'])
                        dest.write(preview.content)
                        # если пост - это одно видео
                        if post['node']['is_video']:
                            # article.videocover.save(fname, dest)
                            # todo убрать создание фотографии, добавить парсинг текста
                            photo = models.Photo.objects.create(article=article)
                            photo.photo.save(fname, dest)
                            photo.save()
                        # если пост - это однфа картинка,ее нужно сохранить в слайдер
                        else:
                            photo = models.Photo.objects.create(article=article)
                            photo.photo.save(fname, dest)
                            photo.save()
                        article.cover.save(fname, dest)
                    article.title = title
                    article.content = text
                    article.save()
                # иначе, если пост - это карусель
                else:
                    items = post['node']['edge_sidecar_to_children']['edges']
                    # флаг для создания обложки новости и видео, чтобы сохранить первое фото из карусели, если фото нет, то дефолтное фото
                    img_exists = False
                    # флаг для создания одного видео
                    video_exists = False
                    for j, item in enumerate(items):
                        element = item['node']
                        fname = f'{element["id"]}.jpg'
                        # если текущий элемент карусели - видео
                        # if element['is_video']:
                        #     if not video_exists:
                        #         article.videolink = element['display_url']
                        #         file = os.path.join(settings.MEDIA_ROOT, 'images', 'covers', fname)
                        #         with open(file, 'wb+') as dest:
                        #             img = requests.get(element['display_url'])
                        #             dest.write(img.content)
                        #             article.videocover.save(fname, dest)
                        #             video_exists = True
                        # если текущий элемент карусели - картинка
                        if not element['is_video']:
                            file = os.path.join(settings.MEDIA_ROOT, 'images', 'articles', fname)
                            with open(file, 'wb+') as dest:
                                img = requests.get(element['display_url'])
                                dest.write(img.content)
                                if not img_exists:
                                    article.cover.save(fname, dest)
                                    img_exists = True
                                # photo_field = File(dest)
                                # photo = models.Photo.objects.create(article=article, photo=photo_field)
                                photo = models.Photo.objects.create(article=article)
                                photo.photo.save(fname, dest)
                                photo.save()
                    article.title = title
                    article.content = text
                    article.save()
    except Exception as error:
        filename = os.path.join('/www', 'dom_miloserdia_api', 'logs', 'import_instaposts_log.txt')
        try:
            with open(filename, 'a', encoding='utf-8') as inp:
                inp.write(
                    str(datetime.datetime.now()) + str(error) + "\n")
            logging.error(_get_detail_exception_info(error))
        except Exception as err:
            print(err)


def fix_articles():
    articles = models.Article.objects.filter(kind__pk=3)
    for a in articles:
        a.content = a.content.replace('Реквизиты', '<a href="#reqv">Реквизиты</a>').replace('реквизиты',
                                                                                            '<a href="#reqv">реквизиты</a>') + '\n\nИсточник: <a href="https://www.instagram.com/dommi_loserdie/">https://www.instagram.com/dommi_loserdie/</a>'
        a.save()


def _get_detail_exception_info(exception_object: Exception):
    """
    Returns the short occurred exception description.
    :param exception_object:
    :return:
    """
    type, value, traceback = sys.exc_info()
    if traceback:
        # import traceback as tb
        # tb.print_tb(traceback, file=sys.stdout)

        return '{message} ({code} in {file}: {line})'.format(
            message=str(exception_object),
            code=exception_object.__class__.__name__,
            file=os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1],
            line=sys.exc_info()[2].tb_lineno,
        )
    else:
        return f'{str(exception_object)} ({exception_object.__class__.__name__})'
