from django.shortcuts import render, redirect
from .models import *
# Create your views here.
def index(request):

	if request.session.get('errors') == None:
		request.session['errors'] = []
	return render(request, 'wish_app/index.html')

def register(request):

	if request.method == 'POST':
		errors = User.objects.register_validation(request.POST)
		print errors
	if len(errors) != 0:
		request.session['errors'] = errors
		return redirect('/')
	else: 
		user = User.objects.register(request.POST)
		request.session['user_id'] = user.id
		request.session['name'] = user.name
		return redirect('/dashboard')	
		print User.objects.all()

def login(request):

	errors = User.objects.login_validation(request.POST)
	if len(errors) != 0:
		request.session['errors'] = errors
		
		for error in errors:
			print error
		return redirect('/dashboard')
	else:
		user= User.objects.login(request.POST)
		request.session['user_id'] = user.id
		request.session['name'] = user.name
		return redirect('/dashboard')

def logout(request):
	request.session.clear()
	return redirect('/')

def dashboard(request):
	user = User.objects.get(id =request.session['user_id'])
	context = {
	"user" : user,
	"myItems": user.added_items.all(),
	"added" : user.wishes.all(),
	"otherItems" : Wish.objects.exclude(added_by = user.id),

	}

	return render(request, 'wish_app/wishlist.html', context)

def new_item(request):

	return render(request, 'wish_app/addwish.html')

def add_wish(request):

	Wish.objects.addItem(request.POST, request.session['user_id'])
	return redirect('/dashboard')

def add_item(request, item_id, user_id):
	Wish.objects.get(id = item_id).added_by.add(user_id)
	return redirect('/dashboard')


def remove_wish(request, item_id):
	user_id = request.session['user_id']
	Wish.objects.get(id=item_id).added_by.remove(user_id)
	return redirect('/dashboard')

def wish_item(request, item_id):

	context={
		'item': Wish.objects.get(id=item_id),
		# 'wish': Wish.objects.filter(wish_id=item_id),
		'others' : Wish.objects.get(id= item_id).added_by.all()
	}
	return render(request, 'wish_app/wishitem.html', context)

def delete(request, item_id):

	Wish.objects.get(id=item_id).delete()
	return redirect('/dashboard')






