import logging
import traceback
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import exception_handler
from django.http import JsonResponse

logger = logging.getLogger(__name__)

class CustomExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        return response
    
    def process_exception(self, request, exception):
        # Log the exception
        logger.error(f"Unhandled exception: {str(exception)}")
        logger.error(traceback.format_exc())
        
        # Return a user-friendly error response
        return JsonResponse({
            'error': 'Internal server error',
            'message': 'Something went wrong. Please try again later.',
            'status_code': 500
        }, status=500)

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)
    
    if response is not None:
        # Customize the error response
        response.data = {
            'error': response.status_code,
            'message': response.data.get('detail', str(response.data)),
            'data': response.data
        }
    
    return response