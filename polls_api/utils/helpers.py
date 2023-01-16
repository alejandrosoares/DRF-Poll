def convert_queryset_to_list_id(queryset):
    list_id = [i.id for i in queryset]
    return list_id