from django import template

#HELPER-FUNCTIONS TEMPLATE

register = template.Library()


#index of lists
@register.filter
def index(indexable, i):
    return indexable[i]


# #get elements with key=name
# @register.filter
# def get_numbers(mylist, name):
#     output = []
#     for i in mylist:
#         output.append(i[name])
#     return output
