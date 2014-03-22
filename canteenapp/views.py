from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from datetime import datetime
from django.contrib import auth
from django.template import RequestContext
from canteenapp.forms import UserForm, UserProfileForm, add_number
from canteenapp.forms import CountForm, UserUpdateForm, itemUpdateForm
from canteenapp.models import UserProfile, orderDetails
from django.core.context_processors import csrf
from canteenapp.models import Food_item
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
#import pdb


def home(request):
    return render_to_response('home.html')


@login_required
def index(request):
    items = Food_item.objects.all()
    #pdb.set_trace()
    userprofile = UserProfile.objects.get(user=request.user)
    q = RequestContext(request, {
                        'item': items})
    return render_to_response('index.html',
        {'full_name': userprofile.Name, 'Credit': userprofile.Credit},
        context_instance=q)


@login_required
@csrf_exempt
def itemconfirmation(request, itemname):
    item = Food_item.objects.get(itemName=itemname)
    saved = False
    if request.user.is_authenticated():
        userprofile = UserProfile.objects.get(user=request.user)
    if not userprofile.Credit <= 0:
        if request.method == 'POST':
            count_form = CountForm(data=request.POST)
            if count_form.is_valid():
                countform = count_form.save(commit=False)
                countform.useradno = userprofile.Admn_no
                countform.itemname = item.itemName
                countform.order_date = datetime.today()
                no_now = item.number
                no_now -= countform.count
                item.number = no_now
                item.save()
                no_of_item = countform.count
                total_cost = no_of_item * item.cost
                credit_now = userprofile.Credit
                credit_now = credit_now - total_cost
                userprofile.Credit = credit_now
                userprofile.save()
                countform.save()
                saved = True
                return HttpResponseRedirect('/saved')
        else:
            count_form = CountForm()
        if not saved:
            c = RequestContext(request, {
                            'item': item, 'count_form': count_form})
            return render_to_response('itemconfirmation.html',
                         context_instance=c)
    else:
        return render_to_response('nobal.html')


@login_required
@csrf_exempt
def update_user_credit(request):
    updated = False
    if request.method == 'POST':
        update = UserUpdateForm(data=request.POST)
        #pdb.set_trace()
        if update.is_valid():
            try:
                userprofile = UserProfile.objects.get(Admn_no=
                                update.cleaned_data['useradno'])
                userprofile.Credit += update.cleaned_data['add_credit']
                userprofile.save()
                updated = True
            except UserProfile.DoesNotExist:
                return render_to_response('invalid_user.html')
    else:
        update = UserUpdateForm()
    if not updated:
        c = RequestContext(request, {
                    'userupdate': update})
        return render_to_response('update_user_credit.html',
                         context_instance=c)
    else:
        return HttpResponseRedirect('/updated')


def  login(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('login.html', c)


def  admin_login(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('admin_login.html', c)


def  admin_auth_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_superuser:
        auth.login(request, user)
        return HttpResponseRedirect('/admin_page')
    else:
        return HttpResponseRedirect('/invalid_admin')


def  auth_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    if user is not None:
        auth.login(request, user)
        return HttpResponseRedirect('/fooditems')
    else:
        return HttpResponseRedirect('/invalid')


def invalid_login(request):
    return render_to_response('invalid.html')


def invalid_admin(request):
    return render_to_response('invalid_admin.html')


@login_required
def admin_page(request):
    return render_to_response('admin_page.html')


@login_required
def updated(request):
    return render_to_response('updated.html')


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')


def register_user(request):
    context = RequestContext(request)
    registered = False
    if request.method == 'POST':
        #pdb.set_trace()
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            registered = True
        if registered:
            return render_to_response('register_success.html')
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render_to_response(
            'register.html',
            {'user_form': user_form, 'profile_form': profile_form,
            'registered': registered},
            context)


def  register_success(request):
    return render_to_response('register_success.html')


@login_required
def  saved(request):
    return render_to_response('saved.html')


@login_required
def order_today(request):
    order_detail = orderDetails.objects.all()
    dated = str(datetime.today())[:-15]
    c = RequestContext(request, {
                    'order_details': order_detail, 'date': dated})
    return render_to_response('order_today.html', context_instance=c)


@login_required
@csrf_exempt
def add_item(request):
    context = RequestContext(request)
    added = False
    if request.method == 'POST':
        #pdb.set_trace()
        item_update = itemUpdateForm(data=request.POST)
        if item_update.is_valid():
            update = item_update.save(commit=False)
            update.pub_date = datetime.today()
            update.save()
            added = True
        if added:
            return render_to_response('item_added.html')
    else:
        item_update = itemUpdateForm()
    return render_to_response(
            'item_update.html',
            {'item_update_form': item_update}, context)


@login_required
@csrf_exempt
def edit_item(request):
    items = Food_item.objects.all()
    q = RequestContext(request, {
                        'item': items})
    return render_to_response('item_list_admin.html', context_instance=q)


@login_required
@csrf_exempt
def add_nos(request, itemname):
    edited = False
    item = Food_item.objects.get(itemName=itemname)
    if request.method == 'POST':
        addnos = add_number(data=request.POST)
        if addnos.is_valid():
            item.number += addnos.cleaned_data['number']
            edited = True
            item.save()
            return HttpResponseRedirect('/saved')
    else:
        addnos = add_number()
    if not edited:
        c = RequestContext(request, {'item': item, 'addnos': add_number})
        return render_to_response('addnos.html', context_instance=c)


