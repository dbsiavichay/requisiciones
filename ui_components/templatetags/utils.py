from django.utils.encoding import force_text

def get_attribute(instance, field):
    names = field.split('.')
    name = names.pop(0)

    if len(names) == 0:
        if not name:
            return None        
        attr = instance if name == 'object' else getattr(instance, name)        
        if attr is None:
            return ''
        if callable(attr):
            return force_text(attr())
        return force_text(attr)
 
    return get_attribute(getattr(instance, name), '.'.join(names))

def get_data(object_list, fields):
    data = []   
    for obj in object_list:        
        line = {field: get_attribute(obj, field) for field in fields}
        line.update({'pk': obj.id, 'id': obj.id, 'url': obj.get_absolute_url(),})
        data.append(line)
    return data