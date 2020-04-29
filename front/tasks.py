import os

import requests
# from PIL import Image

from django.core.files import File

from django.conf import settings
from front import models


sett = models.Settings.objects.get()
url = sett.rapidapi_url.format(iid=sett.instagram_id)
headers = sett.rapidapi_header


def update_lenta():
    try:
        response = requests.get(url, headers=headers)
        response_json = response.json()
        posts = response_json['edges']
        for i, post in enumerate(posts):
            post_id = posts[i]['node']['id']
            article, new = models.Article.objects.get_or_create(instagram_id=post_id)
            if new:
                text = posts[i]['node']['edge_media_to_caption']['edges'][0]['node']['text']
                title = f"{text.split(' ')[0]} {text.split(' ')[1]} {text.split(' ')[2]} {text.split(' ')[3]}..."
                # если пост - это одно видео или одна картинка
                if not 'edge_sidecar_to_children' in posts[i]['node']:
                    # если пост - это одно видео
                    if posts[i]['node']['is_video'] == 'True':
                        video_link = posts[i]['node']['video_url']
                        article.videolink = video_link

                    fname = f'{posts[i]["node"]["id"]}.jpg'
                    cover = os.path.join(settings.MEDIA_ROOT, 'images', 'covers', fname)
                    with open(cover, 'wb+') as dest:
                        preview = requests.get(posts[i]['node']['display_url'])
                        dest.write(preview.content)
                        # если пост - это одно видео
                        if posts[i]['node']['is_video'] == 'True':
                            article.videocover.save(fname, dest)
                        # если пост - это однфа картинка,ее нужно сохранить в слайдер
                        else:
                            photo = models.Photo.objects.create(article=article)
                            photo.photo.save(fname, dest)
                            photo.save()
                        article.cover.save(fname, dest)
                    article.kind = models.ArticleKind.objects.get(pk=3)
                    article.title = title
                    article.content = text
                    article.save()
                # иначе, если пост - это карусель
                else:
                    items = posts[i]['node']['edge_sidecar_to_children']['edges']
                    # флаг для создания обложки новости и видео, чтобы сохранить первое фото из карусели, если фото нет, то дефолтное фото
                    img_exists = False
                    # флаг для создания одного видео
                    video_exists = False
                    for j, item in enumerate(items):
                        element = item[j]['node']
                        fname = f'{element["id"]}.jpg'
                        # если текущий элемент карусели - видео
                        if element['is_video'] == 'True':
                            if not video_exists:
                                article.videolink = element['display_url']
                                file = os.path.join(settings.MEDIA_ROOT, 'images', 'covers', fname)
                                with open(file, 'wb+') as dest:
                                    img = requests.get(element['display_url'])
                                    dest.write(img.content)
                                    article.videocover.save(fname, dest)
                                    video_exists = True
                        # если текущий элемент карусели - картинка
                        else:
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
        pass

