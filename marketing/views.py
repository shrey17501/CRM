from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import *
from .models import *
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required,user_passes_test

users_in_group1 = Group.objects.get(name="MARKETING").user_set.all()
users_in_group2 = Group.objects.get(name="TECHNICAL").user_set.all()


def technicalregister_user(request):
	if request.method == 'POST':
		form = TechnicalSignUpForm(request.POST)
		if form.is_valid():
			form.save()
			# Authenticate and login
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			technical_group = Group.objects.get_or_create(name='TECHNICAL')
			technical_group[0].user_set.add(user)
			login(request, user)
			messages.success(request, "You Have Successfully Registered! Welcome!")
			return redirect('adminhome')
	else:
		form = TechnicalSignUpForm()
		return render(request, 'technicalregister.html', {'form':form})

	return render(request, 'technicalregister.html', {'form':form})

def register_user(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			# Authenticate and login
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			marketing_group = Group.objects.get_or_create(name='MARKETING')
			marketing_group[0].user_set.add(user)
			login(request, user)
			messages.success(request, "You Have Successfully Registered! Welcome!")
			return redirect('adminhome')
	else:
		form = SignUpForm()
		return render(request, 'register.html', {'form':form})

	return render(request, 'register.html', {'form':form})

def is_marketing(user):
    return user.groups.filter(name='MARKETING').exists()

def is_technical(user):
    return user.groups.filter(name='TECHNICAL').exists()


def home(request):
	#leads = Lead.objects.all()
	# Check to see if logging in
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		# Authenticate
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			if user in users_in_group1:
				messages.success(request, "You Have Been Logged In!")
				return redirect('marketinghome')
			elif user in users_in_group2:
				messages.success(request, "You Have Been Logged In!")
				return redirect('technicalhome')
			else:
				messages.success(request, "You Have Been Logged In!")
				return redirect('adminhome')
		else:
			messages.success(request, "There Was An Error Logging In, Please Try Again...")
			return redirect('home')
	else:
		return render(request, 'home.html')

@login_required()
@user_passes_test(is_technical)
def technicalhome(request):
	lead = Lead.objects.all()
	leads=[]
	for l in lead:
		if l.status == "CONVERTED" or l.status == "COLD":
			leads.append(l)
	return render(request, 'technicalhome.html', {'leads':leads})

@login_required()
@user_passes_test(is_marketing)
def marketinghome(request):
	leads = Lead.objects.all()
	return render(request, 'marketinghome.html', {'leads':leads})

@login_required()
def adminhome(request):
	leads = Lead.objects.all()
	return render(request, 'adminhome.html', {'leads':leads})


@login_required()
def logout_user(request):
	logout(request)
	messages.success(request, "You Have Been Logged Out...")
	return redirect('home')


@login_required()
def customer_lead(request, pk):
	if request.user.is_authenticated:
		# Look Up Records
		customer_lead = Lead.objects.get(id=pk)
		return render(request, 'lead.html', {'customer_lead':customer_lead})
	else:
		messages.success(request, "You Must Be Logged In To View That Page...")
		return redirect('home')
	
@login_required()
@user_passes_test(is_technical)
def technical_update_lead(request, pk):
	if request.user.is_authenticated:
		# Look Up Records
		customer_lead = Lead.objects.get(id=pk)
		return render(request, 'technical_update_lead.html', {'customer_lead':customer_lead})
	else:
		messages.success(request, "You Must Be Logged In To View That Page...")
		return redirect('home')
	
@login_required()
def adminlead(request, pk):
	if request.user.is_authenticated:
		# Look Up Records
		customer_lead = Lead.objects.get(id=pk)
		return render(request, 'adminlead.html', {'customer_lead':customer_lead})
	else:
		messages.success(request, "You Must Be Logged In To View That Page...")
		return redirect('home')


@login_required()
@user_passes_test(is_marketing)
def delete_lead(request, pk):
	if request.user.is_authenticated:
		delete_it = Lead.objects.get(id=pk)
		delete_it.delete()
		messages.success(request, "Lead Deleted Successfully...")
		return redirect('marketinghome')
	else:
		messages.success(request, "You Must Be Logged In To Do That...")
		return redirect('home')

@login_required()
def admin_delete_lead(request, pk):
	if request.user.is_authenticated:
		delete_it = Lead.objects.get(id=pk)
		delete_it.delete()
		messages.success(request, "Lead Deleted Successfully...")
		return redirect('adminhome')
	else:
		messages.success(request, "You Must Be Logged In To Do That...")
		return redirect('home')
	
@login_required()
@user_passes_test(is_marketing)
def add_lead(request):
	form = AddLeadsForm(request.POST or None)
	if request.user.is_authenticated:
		if request.method == "POST":
			if form.is_valid():
				form.save()
				messages.success(request, "Lead Added...")
				return redirect('marketinghome')
		return render(request, 'add_lead.html', {'form':form})
	else:
		messages.success(request, "You Must Be Logged In...")
		return redirect('home')

@login_required()
@user_passes_test(is_marketing)
def update_lead(request, pk):
	if request.user.is_authenticated:
		current_lead = Lead.objects.get(id=pk)
		form = AddLeadsForm(request.POST or None, instance=current_lead)
		if form.is_valid():
			form.save()
			messages.success(request, "Lead Has Been Updated!")
			return redirect('marketinghome')
		return render(request, 'update_lead.html', {'form':form})
	else:
		messages.success(request, "You Must Be Logged In...")
		return redirect('home')
	

@login_required()
@user_passes_test(is_technical)
def technical_lead(request, pk):
	if request.user.is_authenticated:
		current_lead = Lead.objects.get(id=pk)
		form = AddLeadsForm(request.POST or None, instance=current_lead)
		if form.is_valid():
			form.save()
			messages.success(request, "Lead Has Been Updated!")
			return redirect('technicalhome')
		return render(request, 'technical_lead.html', {'form':form})
	else:
		messages.success(request, "You Must Be Logged In...")
		return redirect('home')

@login_required()	
def admin_update_lead(request, pk):
	if request.user.is_authenticated:
		current_lead = Lead.objects.get(id=pk)
		form = AddLeadsForm(request.POST or None, instance=current_lead)
		if form.is_valid():
			form.save()
			messages.success(request, "Lead Has Been Updated!")
			return redirect('adminhome')
		return render(request, 'admin_update_lead.html', {'form':form})
	else:
		messages.success(request, "You Must Be Logged In...")
		return redirect('home')