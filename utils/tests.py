from django.test import TestCase
import response

# Create your tests here.
class TemplateTestCase(TestCase):
    def test_create_template(self):
        testcases = [
            {
                'context': {},
                'status': 200,
                'message': '',
                'expected': {
                    'status': 'success',
                    'status_code': 200,
                    'message': '',
                    'data': {}
                }
            },
            {
                'context': {'test': 'test'},
                'status': 200,
                'message': 'Test successfully retrieved',
                'expected': {
                    'status': 'success',
                    'status_code': 200,
                    'message': 'Test successfully retrieved',
                    'data': {'test': 'test'}
                }
            },
            {
                'context': {},
                'status': 400,
                'message': 'Test error',
                'expected': {
                    'status': 'error',
                    'status_code': 400,
                    'message': 'Test error',
                    'data': {}
                }
            }
        ]

        for testcase in testcases:
            self.assertEqual(response.create_template(**testcase), testcase['expected'])