from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from projects.models import Project
from food.forms import FoodFormTres, FoodForm, FoodFormComplete
from food.models import FoodRequest


@login_required
def food_form(request):
    projects = Project.objects.all()
    if request.method == "POST":
        food = FoodRequest()
        form = FoodFormTres(request.POST, instance=food)
        try:
            food = form.save()
        except Exception, e:
            print "unable to save food form"
            print e
        try:
            food.FindTotal()
        except Exception, e:
            print "unable to find total"
            print e
        try:
            food.save()
        except Exception, e:
            print "unable to save food"
            print e
        if food:
            return redirect('food.views.get_food', food.id)
    else:
        form = FoodFormTres()
    return render_to_response('food/food_form.html', {'form': form, 'projects': projects}, context_instance=RequestContext(request))


@login_required
def get_food(request, food_id):
    projects = Project.objects.all()
    try:
        food = FoodRequest.objects.get(pk=food_id)
    except Exception, e:
        print "unable to find food item"
        print e
    return render_to_response('food/food_view.html', {'food': food, 'projects': projects}, context_instance=RequestContext(request))


@login_required
def food_received(request, food_id):
    projects = Project.objects.all()
    food = FoodRequest.objects.get(pk=food_id)
    if request.method == "POST":
        form = FoodFormComplete(request.POST, instance=food)
        try:
            food.save()
        except Exception, e:
            print "food went bad"
            print e
        print request.POST['request_completed_bool']
        if request.POST['request_completed_bool'] == '2':
            food.request_completed_bool = True
            food.save()
        elif request.POST['request_completed_bool'] != '3':
            food.request_completed_bool = False
            food.save()
        if food:
            return redirect('food.views.user_food_overview', food_id)
    else:
        form = FoodFormComplete(instance=food)
    return render_to_response('food/food_comp.html', {'form': form, 'food': food, 'projects': projects}, context_instance=RequestContext(request))


@login_required
def food_overview(request):
    projects = Project.objects.all()
    try:
        pending_food = FoodRequest.objects.filter(request_completed_bool=False).order_by('-request_initiated')
    except Exception, e:
        print "could not load pending requests"
        print e
    return render_to_response('food/food_overview.html', {'pending_food': pending_food, 'projects': projects}, context_instance=RequestContext(request))


@login_required
def user_food_overview(request, food_id):
    projects = Project.objects.all()
    food = FoodRequest.objects.get(pk=food_id)
    user_name = food.user
    try:
        user_food = FoodRequest.objects.filter(request_completed_bool=False, user=user_name).order_by('-request_initiated')
    except Exception, e:
        print e
        print "failed to find user's pending food"
    return render_to_response('food/food_userview.html', {'user_food': user_food, 'user_name': user_name, 'projects': projects}, context_instance=RequestContext(request))


@login_required
def food_overview_complete(request):
    projects = Project.objects.all()
    try:
        complete_food = FoodRequest.objects.filter(request_completed_bool=True).order_by('-request_initiated')
    except Exception, e:
        print "could not load finished food"
        print e
    return render_to_response('food/food_overview_complete.html', {'complete_food': complete_food, 'projects': projects}, context_instance=RequestContext(request))


@login_required
def all_food(request):
    projects = Project.objects.all()
    try:
        food_all = FoodRequest.objects.all().order_by('request_completed_bool', '-request_initiated')
    except Exception, e:
        print e
        print "lost all of the food"
    return render_to_response('food/food_all.html', {'food_all': food_all, 'projects': projects}, context_instance=RequestContext(request))
