from django import template
from django.utils.encoding import force_text
from django.template.loader import render_to_string

register = template.Library()


@register.tag(name='table')
def table(parser, token):

    bits = token.split_contents()    

    nodelist = parser.parse(('theaders', 'tfields', 'endtable',)) 
    token = parser.next_token()    


    if 'theaders' in token.contents:
        headers = token.split_contents()[1:]        
        parser.parse(('tfields',))                
        token = parser.next_token()

    if 'tfields' in token.contents:
        fields = token.split_contents()[1:]        
        parser.parse(('endtable',))        
        parser.delete_first_token()

    sequence = parser.compile_filter(bits[2]) 

    return TableNode(sequence, headers, fields)

class TableNode(template.Node):
    def __init__(self, sequence, headers, fields):        
        self.sequence = sequence
        self.headers = headers
        self.fields = fields
        
    def render(self, context):        
        try:
            object_list = self.sequence.resolve(context, True)            
        except VariableDoesNotExist:
            object_list = []

        context_dict = context.push()
        context_dict.update({
            'data':get_data(object_list, self.fields),
            'headers':[header[1:-1] for header in self.headers],
            'fields': self.fields,
        })

        template_directories = [
            'ui_components/table.html'
        ]
        
        liststr = render_to_string(template_directories, context_dict)
        return liststr
                

def get_attribute(instance, field):
    names = field.split('.')
    name = names.pop(0)

    if len(names) == 0:
        if not name:
            return None        

        attr = instance if name == 'object' else getattr(instance, name)        
        
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


#####
@register.inclusion_tag('ui_components/input.html')
def input(field):    
    return {
        'field':field,        
    }

@register.inclusion_tag('datetimepicker.html')
def datepicker(field):    
    return {
        'field':field,        
    }


#Filters
@register.filter(name='hash')
def hash(h, key):     
    return h[key]