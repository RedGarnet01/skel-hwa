from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect
from django.template.defaultfilters import slugify

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


@login_required
def edit_thing(request, id):
    # grab the object...
    thing = Thing.objects.get(id=id)

    # grab the current logged in user and make sure they're the owner of the thing
    if thing.user != request.user:
        raise Http404

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


def create_thing(request):
    form_class = ThingForm

    # if we're coming from a submitted form, do this
    if request.method == 'POST':
        # grab the data from the submitted form and apply to the form
        form = form_class(request.POST)

        if form.is_valid():
            # create an instance but do not save yet
            thing = form.save(commit=False)

            # set the additional details
            thing.user = request.user
            thing.slug = slugify(thing.name)

            # save the object
            thing.save()

            # redirect to our newly created thing
            return redirect('thing_detail', id=thing.id)

    # otherwise just create the form
    else:
        form = form_class()

    return render(request, 'collection/create_thing.html', {
        'form': form,
    })


def browse_by_name(request, initial=None):
    if initial:
        things = Thing.objects.filter(
             name__istartswith=initial).order_by('name')
    else:
        things = Thing.objects.all().order_by('name')

    return render(request, 'search/search.html', {
        'things': things,
        'initial': initial,
    })
