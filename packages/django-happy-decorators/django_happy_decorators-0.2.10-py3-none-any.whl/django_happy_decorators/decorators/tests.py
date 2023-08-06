from django.test import TestCase, RequestFactory
from decorators.rate_limit import rate_limit
from django.contrib.auth.models import User
from django.http import HttpResponse

class TestRateLimit(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test')
        self.factory = RequestFactory()
    
    def test_rate_limit_user(self):
        
        @rate_limit(num_requests=3, time_minutes=1, redirect_url='/rate_limit_exceeded', mode='user')
        def test_function(request):
            return HttpResponse()

        request = self.factory.get('/test_rate_limit')
        request.user = self.user

        # make request and call test_function a few times to test rate limiting
        for i in range(40):
            resp = test_function(request)
            if i < 3:
                self.assertEqual(resp.status_code, 200)
            else:
                self.assertEqual(resp.status_code, 429)
                self.assertEqual(resp.url, '/rate_limit_exceeded')
    
    def test_rate_limit_ip(self):
        
        @rate_limit(num_requests=100, time_minutes=1, redirect_url='/rate_limit_exceeded', mode='ip')
        def test_function(request):
            return HttpResponse()

        request = self.factory.get('/test_rate_limit')
        request.user = self.user
        request.META['REMOTE_ADDR'] = '129.123.123.123'
        
        # make request and call test_function a few times to test rate limiting
        for i in range(110):
            resp = test_function(request)
            if i < 100:
                self.assertEqual(resp.status_code, 200)
            else:
                self.assertEqual(resp.status_code, 429)
                self.assertEqual(resp.url, '/rate_limit_exceeded')

        # simulate another user with a different IP address and make sure they are not rate limited
        request.META['REMOTE_ADDR'] = '129.111.222.333'
        resp = test_function(request)
        self.assertEqual(resp.status_code, 200)


    def test_rate_limit_all(self):
        
        @rate_limit(num_requests=100, time_minutes=1, redirect_url='/rate_limit_exceeded', mode='all')
        def test_function(request):
            return HttpResponse()

        request = self.factory.get('/test_rate_limit')
        request.user = self.user
        request.META['REMOTE_ADDR'] = '129.123.123.123'
        
        # make request and call test_function a few times to test rate limiting
        for i in range(110):
            resp = test_function(request)
            if i < 100:
                self.assertEqual(resp.status_code, 200)
            else:
                self.assertEqual(resp.status_code, 429)
                self.assertEqual(resp.url, '/rate_limit_exceeded')

        # simulate another user with a different IP address and make sure they are not rate limited
        request.META['REMOTE_ADDR'] = '129.111.222.333'
        resp = test_function(request)
        self.assertEqual(resp.status_code, 429)
        
        # simulate another user with the same IP address and make sure they are rate limited

        request.META['REMOTE_ADDR'] = '129.111.222.444'
        resp = test_function(request)
        self.assertEqual(resp.status_code, 429)

    def test_rate_limit_error_message(self):
        error_message = 'TESTING MESSAGE OF Rate limit exceeded'
        
        @rate_limit(num_requests=2, time_minutes=1, 
                    mode='all',
                    error_message=error_message)
        def test_function(request):
            return HttpResponse()

        request = self.factory.get('/test_rate_limit')
        request.user = self.user

        # make request and call test_function a few times to test rate limiting
        for i in range(110):
            resp = test_function(request)
            if i > 2:
                self.assertEqual(resp.status_code, 429)
                self.assertEqual(resp.content, error_message.encode())
        
        
# command to run tests
# python3 manage.py test