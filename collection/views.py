from django.shortcuts import render
from collection.models import Thing


# def index(request):
#     number = 6
#     # don't forget the quotes because it's a string, not an integer
#     thing = "Thing name"
#     return render(request, 'index.html', {
#         'number': number,
#         # don't forget to pass it in, and the last comma
#         'thing': thing,
#     })

# the rewritten view!
def index(request):
    things = Thing.objects.all()
    return render(request, 'index.html', {
        'things': things,
    })
