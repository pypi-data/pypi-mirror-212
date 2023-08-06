from django import template
from tbase_post.models import Post
from pprint import pprint as pp
from django.db.models import F
register = template.Library()



# 创建信息
# https://docs.djangoproject.com/zh-hans/4.2/howto/custom-template-tags/


@register.filter
def cut(value, arg):
    """Removes all values of arg from the given string"""
    return value.replace(arg, "")






# 生成亚马逊推广的banner链接
@register.filter
@register.inclusion_tag("post/extras/amazon_link.html", takes_context=False)
def amazon_link(product_id=None,product_name=None,store_id=None, *args, **kwargs):
    """
     生成亚马逊推广的banner链接


    """
    return {
        "product_id":product_id,
        "store_id":store_id,
        "product_name":product_name,
        "link":f"https://www.amazon.com/dp/{product_id}/?tag={store_id}",
    }




# tags格式化
@register.simple_tag(takes_context=False)
def tag_names(tags=[], limit=5,*args, **kwargs):
    """
    获取标签的名称，限制输出个数,可以用于keyword输出
    """
    # print("tags",tags)
    # tags

    # print("tags", context)
    names=[]
    for item in tags[:limit]:
        names.append(item.name)
        # print("item",item)
        # print("item", item.name)
        # print("item", item.slug)
        # print("item", item.id)
        # print("item", item.get_absolute_url())
    return {"names":names,
            "names_text":",".join(names)}
    pass


# tags格式化
@register.filter
@register.inclusion_tag("post/extras/tags.html", takes_context=False)
def tags(tags=[], *args, **kwargs):
    # print("tags",tags)
    # tags

    # print("tags", context)
    return {"tags":tags}
    pass

# 相关内容推荐
# 根据tags过滤相关内容
"""
主题模板中使用
# 加载
{% load post_extras %}

{% related_post_by_tags tags limit exclude_pk %}

{% related_post_by_tags object.tags 5 %}

"""

@register.inclusion_tag('post/extras/related_post_by_tags.html',
                        takes_context=False)
def related_post_by_tags(tags=[], limit=5,exclude_pk=None):
    try:
        page_obj=tags.similar_objects()[-limit:]
        # slugs = list(tags.slugs())
        # # print("slugs", slugs)
        # # 排除本节点，查询相关的tags
        # if exclude_pk==None:
        #     page_obj = Post.objects.filter(tags__slug__in=slugs).order_by('-pk').distinct()[:limit]
        # else:
        #     page_obj = Post.objects.filter(tags__slug__in=slugs).exclude(
        #         pk=exclude_pk).order_by('-pk').distinct()[:limit]

        # print("page_obj", page_obj)
        return {
            'state': True,
            'link': "context['home_link']",
            'title': "Related Content",
            "page_obj": page_obj,
            # "content": context
        }
    except Exception as e:
        # print(e)
        return {
            'state': False,
            'link': "context['home_link']",
            'title': "Related Content",
            "page_obj": [],
            # "content": context
        }

@register.inclusion_tag('post/extras/last_update.html',
                        takes_context=False)
def last_update( limit=5,exclude_pk=None):
    """
    
    
    """
    try:

        if exclude_pk==None:
            page_obj = Post.objects.all().order_by('-pk').distinct()[:limit]
        else:
            page_obj = Post.objects.all().exclude(
                pk=exclude_pk).order_by('-pk').distinct()[:limit]

        # print("page_obj", page_obj)
        return {
            'state': True,
            'link': "context['home_link']",
            'title': "Last Update",
            "page_obj": page_obj,
            # "content": context
        }
    except Exception as e:
        # print(e)
        return {
            'state': False,
            'link': "context['home_link']",
            'title': "Last Update",
            "page_obj": [],
            # "content": context
        }