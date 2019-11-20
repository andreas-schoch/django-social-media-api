

# def index(request):
#     if request.method == 'GET':
#         return HttpResponse('Hello im a get')
#
#     if request.method == 'POST':
#         return HttpResponse('Hello im a POST')
#
#     return HttpResponse('test')
    # mail.send(
    #     'andreas_schoch@outlook.com',  # List of email addresses also accepted
    #     'students@propulsionacademy.com',
    #     subject='test',
    #     message='Hi there!',
    #     html_message='Hi <strong>there</strong>!',
    # )
    # return HttpResponse(f'Hello to the index {type(test)}')

#
# class IndexClassBased(View):
#     def get(self, request, **kwargs):
#         print(kwargs)
#         return HttpResponse("Hello im a get")
#
#     def post(self, request):
#         return HttpResponse("Hello im a POST")