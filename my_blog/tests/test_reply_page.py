  
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse

from ..forms import ReplyForm
from ..models import Post, Comments
from ..views import comments


class ReplyTestCase(TestCase):
    '''
    Base test case to be used in all `reply_topic` view tests
    '''
    def setUp(self):
        self.username = 'john'
        self.password = '123'
        user = User.objects.create_user(username=self.username, email='john@doe.com', password=self.password)
        self.blog_post = Post.objects.create(title='Python', author=user, body='hello world')
        self.url = reverse('reply', kwargs={'pk': self.blog_post.pk})


class LoginRequiredReplyTests(ReplyTestCase):
    def test_redirection(self):
        login_url = reverse('login')
        response = self.client.get(self.url)
        self.assertRedirects(response, '{login_url}?next={url}'.format(login_url=login_url, url=self.url))


class ReplyTopicTests(ReplyTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)


    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, ReplyForm)

   
class SuccessfulReplyTopicTests(ReplyTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.url, {'reply': 'hello, world!'})

    def test_redirection(self):
        
        topic_posts_url = reverse('post_detail', kwargs={'pk': self.blog_post.pk})
        self.assertRedirects(self.response, topic_posts_url)




class InvalidReplyTopicTests(ReplyTestCase):
    def setUp(self):
        '''
        Submit an empty dictionary to the `reply_topic` view
        '''
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.url, {})

    def test_status_code(self):
        '''
        An invalid form submission should return to the same page
        '''
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)