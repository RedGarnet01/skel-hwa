from django.shortcuts import render, redirect
from collection.forms import ThingForm
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

def thing_detail(request, id):
    # grab the object...
    thing = Thing.objects.get(id=id)

    # and pass to the template
    return render(request, 'collection/thing_detail.html', {
        'thing': thing,
    })

def edit_thing(request, id):
    # grab the object...
    thing = Thing.objects.get(id=id)

    # set the form we're using...
    form_class = ThingForm

    # if we're coming to this view from a submitted form,
    if request.method == 'POST':
        # grab the data from the submitted form
        form = form_class(data=request.POST, instance=thing)

        if form.is_valid():
            # save the new data
            form.save()
            return redirect('thing_detail', id=thing.id)

    # otherwise just create the form
    else:
        form = form_class(instance=thing)

    # and render the template
    return render(request, 'collection/edit_thing.html', {
        'thing': thing,
        'form': form,
    })
