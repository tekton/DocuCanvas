from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from projects.models import Project
from food.forms import FoodFormTres, FoodForm, FoodFormComplete
from food.models import FoodRequest, ShoppingList, ListItem


@login_required
def food_form(request):
    projects = Project.objects.all()
    if request.method == "POST":
        food = FoodRequest()
        form = FoodFormTres(request.POST, instance=food)
        try:
            food = form.save()
        except Exception, e:
            print("unable to save food form")
            print(e)
        try:
            food.FindTotal()
        except Exception, e:
            print("unable to find total")
            print(e)
        try:
            food.save()
        except Exception, e:
            print("unable to save food")
            print(e)
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
        print("unable to find food item")
        print(e)
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
            print("food went bad")
            print(e)
        print(request.POST['request_completed_bool'])
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
        print("could not load pending requests")
        print(e)
    return render_to_response('food/food_overview.html', {'pending_food': pending_food, 'projects': projects}, context_instance=RequestContext(request))


@login_required
def user_food_overview(request, food_id):
    projects = Project.objects.all()
    food = FoodRequest.objects.get(pk=food_id)
    user_name = food.user
    try:
        user_food = FoodRequest.objects.filter(request_completed_bool=False, user=user_name).order_by('-request_initiated')
    except Exception, e:
        print(e)
        print("failed to find user's pending food")
    return render_to_response('food/food_userview.html', {'user_food': user_food, 'user_name': user_name, 'projects': projects}, context_instance=RequestContext(request))


@login_required
def food_overview_complete(request):
    projects = Project.objects.all()
    try:
        complete_food = FoodRequest.objects.filter(request_completed_bool=True).order_by('-request_initiated')
    except Exception, e:
        print("could not load finished food")
        print(e)
    return render_to_response('food/food_overview_complete.html', {'complete_food': complete_food, 'projects': projects}, context_instance=RequestContext(request))

'''
@login_required
def all_food(request):
    projects = Project.objects.all()
    try:
        food_all = FoodRequest.objects.all().order_by('request_completed_bool', '-request_initiated')
    except Exception, e:
        print(e)
        print("lost all of the food")
    return render_to_response('food/food_all.html', {'food_all': food_all, 'projects': projects}, context_instance=RequestContext(request))'''


@login_required
def createList(request):
    try:
        projects = Project.objects.all()
    except Exception, e:
        print(e)
    try:
        items_list = ListItem.objects.filter(shopping_list__isnull=True).order_by('-created')
        items = []
        for item in items_list:
            if item.single_use:
                if item.use_count != 0:
                    pass
                else:
                    items.append(item)
            else:
                items.append(item)
    except Exception, e:
        print(e)
    if request.method == 'POST':
        try:
            print(request.POST)
            shopping_list = ShoppingList()
            shopping_list.name = request.POST['shopping-list-name']
            shopping_list.save()
            for item in request.POST.getlist('item_list'):
                list_item = ListItem.objects.get(pk=item)
                list_item.shopping_list = shopping_list
                list_item.use_count = list_item.use_count + 1
                list_item.save()
                shopping_list.estimated_cost = shopping_list.estimated_cost + list_item.estimated_cost
                shopping_list.total_items = shopping_list.total_items + 1
            shopping_list.save()
            return redirect('food.views.viewList', shopping_list.id)
        except Exception as e:
            print(e)
    return render_to_response('food/create_list.html', {'items': items, 'projects': projects}, context_instance=RequestContext(request))


@login_required
def removeItems(request, list_id):
    if request.method == 'POST':
        for thing in request.POST.getlist('removal-list'):
            try:
                item = ListItem.objects.get(pk=thing)
                item.shopping_list.estimated_cost = item.shopping_list.estimated_cost - item.estimated_cost
                item.shopping_list.total_items = item.shopping_list.total_items - 1
                item.shopping_list.save()
                item.shopping_list = None
                item.save()
            except Exception, e:
                print(e)
    return redirect('food.views.viewList', list_id)


@login_required
def updateList(request, list_id):
    try:
        projects = Project.objects.all()
    except Exception, e:
        print(e)
    try:
        shopping_list = ShoppingList.objects.get(pk=list_id)
    except Exception, e:
        print(e)
    if request.method == 'POST':
        print(request.POST)
        for item_id in request.POST.getlist('item_list'):
            item = ListItem.objects.get(pk=item_id)
            shopping_list.estimated_cost = shopping_list.estimated_cost + item.estimated_cost
            shopping_list.total_items = shopping_list.total_items + 1
            item.shopping_list = shopping_list
            item.use_count = item.use_count + 1
            item.save()
        shopping_list.save()
        return redirect('food.views.viewList', list_id)
    try:
        items_list = ListItem.objects.filter(shopping_list__isnull=True)
        items = []
        for item in items_list:
            if item.single_use:
                if item.use_count != 0:
                    pass
                else:
                    items.append(item)
            else:
                items.append(item)
    except Exception, e:
        print(e)
    return render_to_response('food/update_list.html', {'items': items, 'list': shopping_list, 'projects': projects}, context_instance=RequestContext(request))
    



@login_required
def viewAllLists(request):
    try:
        projects = Project.objects.all()
    except Exception, e:
        print(e)
    try:
        shopping_lists = ShoppingList.objects.all()
    except Exception, e:
        print(e)
    return render_to_response('food/all_lists.html', {'shopping_lists': shopping_lists, 'projects': projects}, context_instance=RequestContext(request))


@login_required
def viewList(request, list_id=1):
    projects = Project.objects.all()
    try:
        shopping_list = ShoppingList.objects.get(pk=list_id)
    except Exception, e:
        shopping_list = ShoppingList(total_items=0, estimated_cost=0)
    try:
        items = ListItem.objects.filter(shopping_list=shopping_list)
    except Exception, e:
        raise e
    return render_to_response('food/view_list.html', {'shopping_list': shopping_list, 'items': items, 'projects': projects}, context_instance=RequestContext(request))


@login_required
def allRequests(request):
    projects = Project.objects.all()
    try:
        shopping_lists = ShoppingList.objects.all()
    except Exception, e:
        print(e)
    try:
        items_list = ListItem.objects.all()
        items = []
        for item in items_list:
            if item.single_use:
                if item.use_count != 0:
                    pass
                else:
                    items.append(item)
            else:
                items.append(item)
    except Exception, e:
        print(e)
    return render_to_response('food/all_requests.html', {'projects': projects, 'items': items, 'lists': shopping_lists}, context_instance=RequestContext(request))


@login_required
def submitRequest(request):
    try:
        projects = Project.objects.all()
    except Exception as e:
        print(e)
    if request.method == 'POST':
        total = int(request.POST['total-items'])
        for i in range(0,total):
            item = ListItem()
            try:
                item.item = request.POST['item_name-' + str(i)]
                item.quantity = int(request.POST.get('quantity-' + str(i), 0))
                item.estimated_cost = float(request.POST.get('cost-' + str(i), 0))
                item.user = User.objects.get(pk=int(request.POST['user']))
                if request.POST.get('single-use-' + str(i)):
                    item.single_use = True
                else:
                    item.single_use = False
                item.save()
            except Exception, e:
                print(e)
        return redirect('food.views.allRequests')
    return render_to_response('food/make_request.html', {'projects': projects}, context_instance=RequestContext(request))
