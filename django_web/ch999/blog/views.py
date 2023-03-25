from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic import ArchiveIndexView, YearArchiveView, MonthArchiveView
from django.views.generic import DayArchiveView, TodayArchiveView

from blog.models import Post

from django.conf import settings

from django.views.generic import FormView
from blog.forms import PostSearchForm
from django.db.models import Q
from django.shortcuts import render

#--- ListView
class PostLV(ListView):
    model = Post
    template_name = 'blog/post_all.html'
    context_object_name = 'posts' # 템플릿 파일로 넘겨주는 객체 리스트에 대한 컨텍스트 변수명 지정 (object_list 역시 계속 사용할 수 있다)
    paginate_by = 2


#--- DetailView
class PostDV(DetailView):
    model = Post
    
    def get_context_data(self, **kwargs): # 컨텍스트 변수를 추가하기 위해 메소드를 오버라이딩
        context = super().get_context_data(**kwargs) # super() 메소드로 기존의 컨텍스트 변수들을 구하고 context에 대입
        context['disqus_short'] = f"{settings.DISQUS_SHORTNAME}" # f-string을 이용하여 disqus_short 변수에 항목값 대입
        context['disqus_id'] = f"post-{self.object.id}-{self.object.slug}"
        context['disqus_url'] = f"{settings.DISQUS_MY_DOMAIN}{self.object.get_absolute_url()}"
        context['disqus_title'] = f"{self.object.slug}"
        return context


#--- ArchiveView
class PostAV(ArchiveIndexView):
    model = Post
    date_field = 'modify_dt'


class PostYAV(YearArchiveView):
    model = Post
    date_field = 'modify_dt'
    make_object_list = True # 해당 연도에 해당하는 객체의 리스트를 만들어서 템플릿에 넘겨준다 default = False


class PostMAV(MonthArchiveView):
    model = Post
    date_field = 'modify_dt'


class PostDAV(DayArchiveView):
    model = Post
    date_field = 'modify_dt'


class PostTAV(TodayArchiveView):
    model = Post
    date_field = 'modify_dt'


class TagCloudTV(TemplateView):
    template_name = 'taggit/taggit_cloud.html'


class TaggedObjectLV(ListView):
    template_name = 'taggit/taggit_post_list.html'
    model = Post
    
    def get_queryset(self):
        return Post.objects.filter(tags__name=self.kwargs.get('tag'))
    
    # template에 넘겨줄 컨텍스트 변수를 추가
    def get_context_data(self, **kwargs):
        # super()~~ 를 호출하여 상위 클래스의 변경 전 컨텍스트 변수를 구한다.
        context = super().get_context_data(**kwargs)
        context['tagname'] = self.kwargs['tag']
        return context
    
#--- FormView
class SearchFormView(FormView):
    form_class = PostSearchForm
    template_name = 'blog/post_search.html'
    
    def form_valid(self, form):
        searchWord = form.cleaned_data['search_word']
        post_list = Post.objects.filter(Q(title__icontains=searchWord) | Q(description__icontains=searchWord) | Q(content__icontains=searchWord)).distinct()
        
        context = {}
        context['form'] = form
        context['search_term'] = searchWord
        context['object_list'] = post_list
        
        return render(self.request, self.template_name, context)