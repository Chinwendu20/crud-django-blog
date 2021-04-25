from django.shortcuts import render, redirect

# Create your views here.

from .models import Post, Comments
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth import login as auth_login
from .forms import SignUpForm, ReplyForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404 

class BlogListView(ListView):
	model=Post
	template_name='home.html'

class BlogDetailView(DetailView):
	model=Post
	template_name = 'post_detail.html'

class BlogCreateView(CreateView):
	model= Post
	template_name='post_new.html'
	fields=['title', 'author', 'body']

class BlogUpdateView(UpdateView):
	model=Post
	template_name='post_edit.html'
	fields=['title', 'body']

class BlogDeleteView(DeleteView):
	model=Post
	template_name='post_delete.html'
	success_url=reverse_lazy('home')
	
def signup(request):
	if request.method == 'POST':
		form=SignUpForm(request.POST)
		if form.is_valid():
			user=form.save()
			auth_login(request, user)
			return redirect('home')
	else:
		form=SignUpForm()
	return render(request, 'signup.html', {'form':form})

@login_required
def comments(request, pk):
    post = Post.objects.get(pk=pk)
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
        	comment=form.save(commit=False)
        	comment.blog_post=post
        	comment=form.save()
        	return redirect('post_detail', pk=pk)
    else:
        form = ReplyForm()
    return render(request, 'reply.html', { 'form': form, 'post':post})