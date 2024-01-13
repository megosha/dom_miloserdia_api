from django.test import TestCase

from front import models, tasks


class TestTasks(TestCase):
    def test_get_from_vk(self):
        models.Settings.objects.create(
            mailto=[],
            vk_group='link',
            vk_token='token'
        )
        models.ArticleKind.objects.create(pk=3)
        count = tasks.get_from_vk()
        self.assertGreater(count, 5)
        self.assertEqual(models.Article.objects.count(), count)
        self.assertGreater(models.Photo.objects.count(), count)
