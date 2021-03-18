from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Question, Profile
from django.contrib.auth.models import User
from .forms import answerForm, UserUpdateForm, ProfileUpdateForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin




# Create your views here.
def index(request):
    context = {
        'questions': Question.objects.all().order_by('-likes', '-created_date'),
    }
    return render(request, 'bitsapp/home.html', context)
    
def login(request):
    return render(request, 'bitsapp/login.html')
    

class ask(LoginRequiredMixin, CreateView):
    model = Question
    template_name = 'bitsapp/quesform.html'
    fields = ['title', 'text']

    def form_valid(self, form):
        form.instance.author=self.request.user
        #form.instance.votes = 0
        #messages.success(self.request,'Your Question is now Posted')
        return super().form_valid(form)

@login_required
def answer(request, **kwargs):
    q = Question.objects.filter(id = kwargs['pk'])[0]
    '''
    if request.user.is_authenticated:
        u = request.user
        usrr = SocialAccount.objects.filter(user = u)[0]
    '''
    
    form = answerForm(request.POST)
    if form.is_valid():
        form.instance.of = q
        form.instance.author = request.user
        form.save()
        return redirect('bitsapp:index')
            
    context = {
        'form': form
    }
            
    return render(request, 'bitsapp/answers_form.html', context)
            
@login_required
def view_answer(request, **kwargs):
    qn = Question.objects.filter(id = kwargs['pk'])[0]
    
    

    likes_connected = get_object_or_404(Question, id=kwargs['pk'])
    liked = False
    if likes_connected.likes.filter(id=request.user.id).exists():
        liked = True
    
    
    return render(request, 'bitsapp/question_detail.html',{'ans':qn.allans.all(), 'question':qn, 'number_of_likes': likes_connected.number_of_likes, 'post_is_liked': liked})
        
def QuestionLike(request, pk):
    post = get_object_or_404(Question, id=request.POST.get('ques_id'))
    
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return HttpResponseRedirect(reverse('bitsapp:view_answer', args=[str(pk)]))
 
@login_required 
def profile(request, **kwargs):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('bitsapp:profile', pk=kwargs['pk'])
        
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user)
        
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'profile': Profile.objects.filter(id = kwargs['pk'])[0],
        'no_of_answers': Profile.objects.filter(id = kwargs['pk'])[0].usr.ansrs.count()
    }

    return render(request, 'bitsapp/profile.html', context)
    