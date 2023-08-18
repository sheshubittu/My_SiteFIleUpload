from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash 
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib import messages 
from .forms import SignUpForm, EditProfileForm 
import openai
import pandas as pd
import io
import json
from django.utils.datastructures import MultiValueDictKeyError


# Create your views here.
def home(request): 
	return render(request, 'authenticate/home.html', {})

def login_user (request):
	if request.method == 'POST': #if someone fills out form , Post it 
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			messages.success(request,('Sucessfully Login...'))
			return redirect('home') 
		else:
			messages.error(request,('Incorrect..'))
			return redirect('login') 
	else:
		return render(request, 'authenticate/login.html', {})

def logout_user(request):
	logout(request)
	messages.success(request,('Logout Succesfully..'))
	return redirect('home')

def register_user(request):
	if request.method =='POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			login(request,user)
			messages.success(request, ('Succefully Registered..'))
			return redirect('home')
	else: 
		form = SignUpForm() 

	context = {'form': form}
	return render(request, 'authenticate/register.html', context)

def edit_profile(request):
	if request.method =='POST':
		form = EditProfileForm(request.POST, instance= request.user)
		if form.is_valid():
			form.save()
			messages.success(request, ('You have edited your profile'))
			return redirect('home')
	else: 		
		form = EditProfileForm(instance= request.user) 

	context = {'form': form}
	return render(request, 'authenticate/edit_profile.html', context)
	#return render(request, 'authenticate/edit_profile.html',{})



def change_password(request):
	if request.method =='POST':
		form = PasswordChangeForm(data=request.POST, user= request.user)
		if form.is_valid():
			form.save()
			update_session_auth_hash(request, form.user)
			messages.success(request, ('You have edited your password'))
			return redirect('home')
	else:
		form = PasswordChangeForm(user= request.user) 

	context = {'form': form}
	return render(request, 'authenticate/change_password.html', context)

def process_data(request): 
	if request.method == 'POST':
		try:
			uploaded_file = request.FILES['csv_file']
		except MultiValueDictKeyError:
			messages.error(request, ('Please select a file.'))
			return render(request, 'authenticate/home.html')
		
		# prompt = request.POST['prompt']
		
		# prompt = "Prepare employee wise ranking and write html code for bar chart with titles" #Working
		# prompt = "Analyze the data and write html code for responsive pie chart with titles"  #Working
		prompt = "Analyze the data and write html code to draw bar chart for district wise total camps with title"
		

		
		
		file_content = uploaded_file.read().decode('utf-8')
		
		df = pd.read_csv(io.StringIO(file_content))
		
		df3 = df.iloc[:10]
		df4 = df3.to_json(orient='records')
		chart_types = request.POST.getlist('chart_type')
		# prompt = "Analyze the data and write HTML code to draw"
		user_input = prompt + df4
		# for chart_type in chart_types:
		# 	prompt += f" {chart_type},"
		# 	prompt = prompt.rstrip(',') + " with title"
		# 	user_input = prompt + df4

		total_length = len(user_input)
		if total_length > 4096:
				messages.error(request, f'Input file exceeds {total_length} the maximum token limit is 4096. Please upgrade the plan')
				return render(request, 'authenticate/home.html')


		
		# openai.api_key = "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"
		openai.api_key = "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"
		response = openai.Completion.create(
			engine="text-davinci-003",
			prompt=user_input,
			max_tokens=1000,
			n=1,
			stop=None,
			temperature=0.5,
		) 
		
		response_text = response.choices[0].text.strip()
		try:
			json_data = json.loads(response_text)
		except json.JSONDecodeError:
			json_data = response_text


		
		response_history = request.session.get('response_history', [])
		response_history.append(response_text)
		request.session['response_history'] = response_history

		
		response_history_last_5 = response_history[-1:]

		generated_html_code = response_text

		
		context = {'json_data': json_data, 'response_history': response_history_last_5, 'csv_file_name': uploaded_file.name, 'generated_html_code': generated_html_code}
		return render(request, 'authenticate/home.html', context)
	else:
		return render(request, 'authenticate/home.html')


def clear_history(request):
    request.session['response_history'] = []
    return render(request, 'authenticate/home.html')

def IndexPage(request): 
	return render(request, 'authenticate/index.html', {})


 