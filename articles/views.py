from . import forms
from django.shortcuts import render, redirect
from .models import Article, Comment
from django.contrib.auth.decorators import login_required
from django.db.models import Q


def home(request):
    search = request.GET.get('search')
    articles = Article.objects.all().order_by('date')
    articles = articles.filter(Q(title__icontains=search) | Q(text__icontains=search)) if search else articles
    return render(request, 'articles_list.html', {'articles': articles})


def article_detail(request, slug):
    article = Article.objects.get(slug=slug)
    form = forms.CommentForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.article = article
        instance.save()
        return redirect('articles:article_detail', slug=article.slug)
    return render(request, 'article_detail.html', {'article': article, 'form': form})


def article_create(request):
    form = forms.ArticleForm(request.POST or None, request.FILES)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.author = request.user
        instance.save()
        return redirect('articles:home')
    return render(request, 'article_create.html', {'form': form})


@login_required(login_url='/users/sign_in')
def edit_article(request, slug):
    article = Article.objects.get(slug=slug)

    if request.user != article.author:
        return render(request, 'error.html', {'article': article})
    form = forms.ArticleForm(request.POST or None, request.FILES or None, instance=article)
    if form.is_valid():
        form.save()
        return redirect('articles:article_detail', slug=request.POST.get('slug'))
    return render(request, 'edit_article.html', {"form": form, 'article': article})


def delete_article(request, slug):
    article = Article.objects.get(slug=slug)
    if request.method == 'POST':
        article.delete()
        return redirect('articles:home')
    return render(request, 'delete_article.html', {'article': article})


def like(request, slug):
    article = Article.objects.get(slug=slug)

    if request.user not in article.likes.all():
        article.likes.add(request.user)
        article.dislikes.remove(request.user)
    elif request.user in article.likes.all():
        article.likes.remove(request.user)
    return redirect('articles:article_detail', slug=slug)


def dislike(request, slug):
    article = Article.objects.get(slug=slug)

    if request.user not in article.dislikes.all():
        article.dislikes.add(request.user)
        article.likes.remove(request.user)
    elif request.user in article.dislikes.all():
        article.dislikes.remove(request.user)
    return redirect('articles:article_detail', slug=slug)


def delete_comment(request, pk):
    comment = Comment.objects.get(pk=pk)

    if request.user != comment.user:
        return render(request, 'error.html', {'comment': comment})

    if request.method == 'POST':
        comment.delete()
        return redirect('articles:article_detail', slug=comment.article.slug)
    return render(request, 'delete_comment.html', {'article': comment.article})


def edit_comment(request, pk):
    comment = Comment.objects.get(pk=pk)
    form = forms.CommentForm(request.POST or None, instance=comment)

    if request.user != comment.user:
        return render(request, 'error.html', {'comment': comment})

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('articles:article_detail', slug=comment.article.slug)
    return render(request, 'edit_comment.html', {'form': form, 'article': comment.article})
