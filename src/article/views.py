from django.contrib.auth import get_user_model
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Sum, Value
from django.db.models.functions import Coalesce

from django.shortcuts import render, get_object_or_404, redirect
from taggit.models import Tag

from article.forms import PostForm, CategoryForm, FriendlyLinkForm
from article.models import Post, Category, FriendlyLink

from django.contrib.auth.decorators import permission_required


# TODO: (get_common_data) ИСПОЛЬЗУЕТСЯ в create post, update post, create cat, update cat,  create link, update link

def get_common_data():
    all_categories = Category.objects.all()
    popular_posts = Post.objects.filter(is_active=True).order_by('-request_count')[:3]
    category_views = Category.objects.annotate(total_views=Coalesce(Sum('posts__request_count'), Value(0)))
    sorted_categories = sorted(category_views, key=lambda x: x.total_views, reverse=True)[:8]
    return {
        'all_categories': all_categories,
        'popular_posts': popular_posts,
        'category_views': category_views,
        'popular_categories': sorted_categories,
    }


def list_posts(request):
    current_url = request.path
    latest_post = Post.objects.order_by('-created_at').first()
    posts = Post.objects.all().order_by('-created_at').select_related('category')
    popular_posts = Post.objects.filter(is_active=True).order_by('-request_count')[:3]
    sidebar_posts = Post.objects.filter(in_trend=True)[:7]

    category_views = Category.objects.annotate(total_views=Coalesce(Sum('posts__request_count'), Value(0)))
    sorted_categories = sorted(category_views, key=lambda x: x.total_views, reverse=True)[:8]

    all_categories = Category.objects.all()

    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        'latest_post': latest_post,
        'posts': posts,
        'popular_posts': popular_posts,
        'sidebar_posts': sidebar_posts,
        'popular_categories': sorted_categories,
        'all_categories': all_categories,
        'current_url': current_url[1:],
    }

    return render(request, 'article/post/list.html', context)


def detail_post(request, slug):
    post = get_object_or_404(Post, slug=slug)

    viewed_post_cookie = request.COOKIES.get('viewed_post_{}'.format(post.id), False)

    if not viewed_post_cookie:
        post.request_count += 1
        post.save()

        popular_posts = Post.objects.filter(is_active=True).order_by('-request_count')[:3]
        friendly = FriendlyLink.objects.all()

        category_views = Category.objects.annotate(total_views=Coalesce(Sum('posts__request_count'), Value(0)))
        sorted_categories = sorted(category_views, key=lambda x: x.total_views, reverse=True)[:8]

        all_categories = Category.objects.all()

        context = {
            'post': post,
            'popular_posts': popular_posts,
            'friendly': friendly,
            'popular_categories': sorted_categories,
            'all_categories': all_categories
        }

        response = render(request, 'article/post/detail.html', context)
        response.set_cookie('viewed_post_{}'.format(post.id), True)
        return response

    popular_posts = Post.objects.filter(is_active=True).order_by('-request_count')[:3]
    friendly = FriendlyLink.objects.all()

    category_views = Category.objects.annotate(total_views=Coalesce(Sum('posts__request_count'), Value(0)))
    sorted_categories = sorted(category_views, key=lambda x: x.total_views, reverse=True)[:8]

    all_categories = Category.objects.all()

    context = {
        'post': post,
        'popular_posts': popular_posts,
        'friendly': friendly,
        'popular_categories': sorted_categories,
        'all_categories': all_categories
    }

    return render(request, 'article/post/detail.html', context)


# TODO: add post
@permission_required('article:create_post', raise_exception=True)
def create_post(request):
    form_of_post = PostForm()
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            owner = request.user

            new_post = form.save(commit=False)
            new_post.owner = owner
            new_post.save()

            return redirect('article:post_list')
    else:
        form_of_post = PostForm()

    common_data = get_common_data()

    context = {
        'form_of_post': form_of_post,
        'title': "Create post",
        **common_data
    }

    return render(request, "article/post/create_post.html", context)


# TODO: update post
@permission_required('article:update_post', raise_exception=True)
def update_post(request, pk):
    common_data = get_common_data()
    post = get_object_or_404(Post, id=pk)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('article:post_list')
        else:
            return render(request, 'article/post/update_post.html')
    else:
        form_of_post = PostForm(instance=post)
        context = {
            'title': "Update",
            'form_of_post': form_of_post,
            **common_data
        }
        return render(request, 'article/post/update_post.html', context)


# TODO: delete post

def delete_post(request, pk):
    post = Post.objects.get(id=pk)
    post.delete()
    return redirect('article:post_list')


# TODO: create Category
@permission_required('article:create_category', raise_exception=True)
def create_category(request):

    form_of_cat = CategoryForm()
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect('article:post_list')
    else:
        form_of_cat = CategoryForm()

    common_data = get_common_data()

    context = {
        'form_of_cat': form_of_cat,
        'title': "Create category",
        **common_data
    }

    return render(request, "article/category/create_category.html", context)


# TODO: update category
@permission_required('article:update_post', raise_exception=True)
def update_category(request, pk):

    common_data = get_common_data()

    category = get_object_or_404(Category, id=pk)

    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('article:post_list')
        else:
            return render(request, 'article/post/update_post.html')
    else:
        form_of_cat = CategoryForm(instance=category)
        context = {
            'title': "Update category",
            'form_of_cat': form_of_cat,
            **common_data
        }
        return render(request, 'article/category/category_update.html', context)


# TODO: category detail
def category_detail(request, category_slug):
    current_url = request.path
    category = get_object_or_404(Category, slug=category_slug)
    initial_posts = category.posts.all().order_by('-created_at')
    popular_posts = Post.objects.filter(is_active=True).order_by('-request_count')[:3]
    friendly = FriendlyLink.objects.all()

    category_views = Category.objects.annotate(total_views=Coalesce(Sum('posts__request_count'), Value(0)))
    sorted_categories = sorted(category_views, key=lambda x: x.total_views, reverse=True)[:8]

    all_categories = Category.objects.all()

    paginator = Paginator(initial_posts, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        'category': category,
        'popular_posts': popular_posts,
        'posts': posts,
        'friendly': friendly,
        'popular_categories': sorted_categories,
        'all_categories': all_categories,
        'current_url': current_url,
    }

    return render(request, 'article/category/category_detail.html', context)


# TODO: create FriendlyLink
@permission_required('article:create_link', raise_exception=True)
def create_link(request):

    form_of_link = FriendlyLinkForm()
    if request.method == "POST":
        form = FriendlyLinkForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect('article:post_list')
    else:
        form_of_link = FriendlyLinkForm()

    common_data = get_common_data()

    context = {
        'form_of_link': form_of_link,
        'title': "Create link",
        **common_data
    }

    return render(request, "article/friendlyLink/create_link.html", context)


# TODO: TAGS
def tag_list(request, tag_slug=None):
    post_list = Post.objects.all()
    popular_posts = Post.objects.filter(is_active=True).order_by('-request_count')[:3]
    friendly = FriendlyLink.objects.all()

    all_categories = Category.objects.all()
    category_views = Category.objects.annotate(total_views=Coalesce(Sum('posts__request_count'), Value(0)))
    sorted_categories = sorted(category_views, key=lambda x: x.total_views, reverse=True)[:8]

    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        'posts': posts,
        'tag': tag,
        'popular_posts': popular_posts,
        'friendly': friendly,
        'popular_categories': sorted_categories,
        'all_categories': all_categories
    }

    return render(request, 'article/post/post_tags.html', context)
