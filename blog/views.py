from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .models import Post, Comment #<- Chapter 02

#Chapter 02
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count

# class PostListView(ListView):
#     queryset = Post.pub.all()
#     context_object_name = 'posts'
#     paginate_by = 3
#     template_name = 'blog/post/list.html'

# The original function to make a list of posts with Pagination

def post_list(request, tag_slug=None):
    object_list = Post.pub.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])
    paginator = Paginator(object_list, 3)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context = {
        'page': page,
        'posts': posts,
        'tag': tag
    }
    return render(request, 'blog/post/list.html', context)
    

def post_detail(request, year, month, day, post_):
    post = get_object_or_404(Post, slug=post_,status='published',publish__year=year,publish__month=month,publish__day=day)
    
    #Chapter 02
    comments = post.comments.filter(active=True)
    new_comment = None   
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()

    post_tags_id = post.tags.values_list('id', flat=True) #Gte the tags of the post - Return: [(1,), (2,), ...] but with flat -> [1,2,3,...]
    similar_posts = Post.pub.filter(tags__in=post_tags_id).exclude(id=post.id) #get teh posts with that tags or similar (exluding actual)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags' ,'-publish')[:4] #get 

    context = {
        'post': post,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form':comment_form,
        'similar_posts': similar_posts
    }

    return render(request, 'blog/post/detail.html', context)    
    

#Chapter 02
def post_share(request, post_id):

    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url} \n\n"
            send_mail(subject, message, 'chivas9840@gmail.com', [cd['to']])
            sent = True

    else:
        form = EmailPostForm()
    context = {
        'post': post,
        'form': form,
        'sent': sent
    }
    return render(request, 'blog/post/share.html', context)
