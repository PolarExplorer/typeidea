from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Post, Category, Tag
from .adminforms import PostAdminForm

from typeidea.custom_site import custom_site


class PostInline(admin.TabularInline):
    fields = ('title', 'desc')
    extra = 1 
    model = Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [PostInline, ]

    list_display = ('name', 'status', 'is_nav', 'owner', 'created_time', 'post_count')
    fields = ('name', 'status', 'is_nav')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(CategoryAdmin, self).save_model(request, obj, form, change)

    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_description = '文章数量'
    


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'created_time')
    fields = ('name', 'status')
    
    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(TagAdmin, self).save_model(request, obj, form, change)
    

class CategoryOwnerFilter(admin.SimpleListFilter):
    """自定义过滤器只展示当前用户分类"""

    title = '分类过滤器'                # 展示标题
    parameter_name = 'owner_category'   # 查询时URL参数的名字

    def lookups(self, request, model_admin):    # 返回要展示的内容和查询用的id
        return Category.objects.filter(owner=request.user).values_list('id', 'name')

    def queryset(self, request, queryset):      # 根据URL Query的内容返回列表页数据
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=self.value())
        return queryset


@admin.register(Post, site=custom_site)
class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    
    list_display = [
        'title', 'category', 'status',
        'created_time', 'operator'
    ]
    list_display_links = []

    list_filter = [CategoryOwnerFilter]
    search_fields = ['title', 'category_name']

    actions_on_top = True
    actions_on_button = True

    # 编辑页面
    save_on_top = True

    exclude = ('owner',)

#    fields = (                 # 1.限制要展示的字段 2.配置展示字段的顺序
#        ('category', 'title'),
#        'desc',
#        'status',
#        'content',
#        'tag',
#    )

    fieldsets = (
        ('基础配置', {
            'description': '基础配置描述',
            'fields':(                      # 1.控制展示哪些元素 2.给元素排序并组合元素的位置
                ('title', 'category'),
                'status',
            ),
        }),
        ('内容', {
            'fields': (
                'desc',
                'content',
            ),
        }),
        ('额外信息', {
            'classes': ('collapse',),       # 给要配置的版块加CSS属性
            'fields': ('tag', ),
        })
    )

    filter_horizontal = ('tag', )

    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('cus_admin:blog_post_change', args=(obj.id,))
        )
    operator.short_description = '操作'

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(PostAdmin, self).save_model(request, obj, form, change)
    
    def get_queryset(self, request):
        qs = super(PostAdmin, self).get_queryset(request)
        return qs.filter(owner=request.user)
    
    class Media:
        css = {
            'all': ("https://cdn.bootcdn.net/ajax/libs/twitter-bootstrap/4.5.0/css/bootstrap.min.css")
        }
        js = ("https://cdn.bootcdn.net/ajax/twitter-bootstrap/4.5.0/js/bootstrap.bundle.js")



















