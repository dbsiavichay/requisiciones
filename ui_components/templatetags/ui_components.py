from django import template
from django.utils.encoding import force_text
from django.template.loader import render_to_string


from django.utils.safestring import mark_safe
import re

from django.template import Context
from django.template.base import (     
    FILTER_SEPARATOR, VariableNode, TextNode,
    Node, NodeList, TemplateSyntaxError, VariableDoesNotExist,    
)

register = template.Library()


class TableNode(Node):
    child_nodelists = ('nodelist_headers', 'nodelist_loop', 'nodelist_empty')

    def __init__(self, loopvars, sequence, is_reversed, nodelist_headers, nodelist_loop, nodelist_empty=None):        
        self.loopvars, self.sequence = loopvars, sequence
        self.is_reversed = is_reversed
        self.nodelist_headers, self.nodelist_loop = nodelist_headers, nodelist_loop
        if nodelist_empty is None:
            self.nodelist_empty = NodeList()
        else:
            self.nodelist_empty = nodelist_empty


    def __repr__(self):
        reversed_text = ' reversed' if self.is_reversed else ''
        return "<Table Node: ui_table %s in %s, tail_len: %d%s>" % \
            (', '.join(self.loopvars), self.sequence, len(self.nodelist_loop),
             reversed_text)

    def __iter__(self):        
        for node in self.nodelist_loop:
            yield node
        for node in self.nodelist_empty:
            yield node

    def render(self, context):        
        self.nodelist_headers = [node for node in self.nodelist_headers if isinstance(node, VariableNode)]
        self.nodelist_loop = [node for node in self.nodelist_loop if not isinstance(node, TextNode)]

        len_nodelist_headers = len(self.nodelist_headers)
        len_nodelist_loop = len(self.nodelist_loop)

        if len_nodelist_headers != len_nodelist_loop:
            raise ValueError(
                "There are {} headers and {} column values, need the same length"
                .format(len_nodelist_headers, len_nodelist_loop),
            )

        if 'forloop' in context:
            parentloop = context['forloop']
        else:
            parentloop = {}
        with context.push():
            try:
                values = self.sequence.resolve(context, True)
            except VariableDoesNotExist:
                values = []
            if values is None:
                values = []
            if not hasattr(values, '__len__'):
                values = list(values)
            len_values = len(values)            
            if len_values < 1:
                return self.nodelist_empty.render(context)
            
            if self.is_reversed:
                values = reversed(values)
            num_loopvars = len(self.loopvars)
            unpack = num_loopvars > 1
            # Create a forloop value in the context.  We'll update counters on each
            # iteration just below.
            loop_dict = context['forloop'] = {'parentloop': parentloop}            

            rows = []
            for i, item in enumerate(values):
                # Shortcuts for current loop iteration number.                
                loop_dict['counter'] = i + 1
                # Reverse counter iteration numbers.
                loop_dict['revcounter'] = len_values - i                
                # Boolean values designating first and last times through loop.
                loop_dict['first'] = (i == 0)
                loop_dict['last'] = (i == len_values - 1)

                pop_context = False
                if unpack:
                    # If there are multiple loop variables, unpack the item into
                    # them.
                    try:
                        len_item = len(item)
                    except TypeError:  # not an iterable
                        len_item = 1
                    # Check loop variable count before unpacking
                    if num_loopvars != len_item:
                        raise ValueError(
                            "Need {} values to unpack in for loop; got {}. "
                            .format(num_loopvars, len_item),
                        )
                    unpacked_vars = dict(zip(self.loopvars, item))
                    pop_context = True
                    context.update(unpacked_vars)
                else:                    
                    context[self.loopvars[0]] = item                                

                row = []
                for node in self.nodelist_loop:                    
                    result = node.render_annotated(context)                    
                    t = context.template.engine.get_template('ui_components/table/td.html')
                    td = t.render(Context({'td': result}, autoescape=context.autoescape))                                        
                    row.append(td)

                t = context.template.engine.get_template('ui_components/table/tr.html')
                tr = t.render(Context({'row': row}, autoescape=context.autoescape))
                rows.append(tr)

                if pop_context:
                    # The loop variables were pushed on to the context so pop them
                    # off again. This is necessary because the tag lets the length
                    # of loopvars differ to the length of each set of items and we
                    # don't want to leave any vars from the previous loop on the
                    # context.
                    context.pop()
            
            headers = []
            for node in self.nodelist_headers:
                header = node.render_annotated(context)
                headers.append(header)            

            t = context.template.engine.get_template('ui_components/table/table.html')
            table = t.render(Context({ 'headers':headers, 'rows': rows}, autoescape=context.autoescape))            
        
        return mark_safe(table)

@register.tag('ui_table')
def do_table(parser, token):
    """
    Loops over each item in an array.

    For example, to display a list of athletes given ``athlete_list``::

        <ul>
        {% for athlete in athlete_list %}
            <li>{{ athlete.name }}</li>
        {% endfor %}
        </ul>

    You can loop over a list in reverse by using
    ``{% for obj in list reversed %}``.

    You can also unpack multiple values from a two-dimensional array::

        {% for key,value in dict.items %}
            {{ key }}: {{ value }}
        {% endfor %}

    The ``for`` tag can take an optional ``{% empty %}`` clause that will
    be displayed if the given array is empty or could not be found::

        <ul>
          {% for athlete in athlete_list %}
            <li>{{ athlete.name }}</li>
          {% empty %}
            <li>Sorry, no athletes in this list.</li>
          {% endfor %}
        <ul>

    The above is equivalent to -- but shorter, cleaner, and possibly faster
    than -- the following::

        <ul>
          {% if athlete_list %}
            {% for athlete in athlete_list %}
              <li>{{ athlete.name }}</li>
            {% endfor %}
          {% else %}
            <li>Sorry, no athletes in this list.</li>
          {% endif %}
        </ul>

    The for loop sets a number of variables available within the loop:

        ==========================  ================================================
        Variable                    Description
        ==========================  ================================================
        ``forloop.counter``         The current iteration of the loop (1-indexed)
        ``forloop.counter0``        The current iteration of the loop (0-indexed)
        ``forloop.revcounter``      The number of iterations from the end of the
                                    loop (1-indexed)
        ``forloop.revcounter0``     The number of iterations from the end of the
                                    loop (0-indexed)
        ``forloop.first``           True if this is the first time through the loop
        ``forloop.last``            True if this is the last time through the loop
        ``forloop.parentloop``      For nested loops, this is the loop "above" the
                                    current one
        ==========================  ================================================
    """
    bits = token.split_contents()
    if len(bits) < 4:
        raise TemplateSyntaxError("'ui_table' statements should have at least four"
                                  " words: %s" % token.contents)

    is_reversed = bits[-1] == 'reversed'
    in_index = -3 if is_reversed else -2
    if bits[in_index] != 'in':
        raise TemplateSyntaxError("'ui_table' statements should use the format"
                                  " 'ui_table x in y': %s" % token.contents)

    invalid_chars = frozenset((' ', '"', "'", FILTER_SEPARATOR))
    loopvars = re.split(r' *, *', ' '.join(bits[1:in_index]))    
    for var in loopvars:
        if not var or not invalid_chars.isdisjoint(var):
            raise TemplateSyntaxError("'ui_table' tag received an invalid argument:"
                                      " %s" % token.contents)

    sequence = parser.compile_filter(bits[in_index + 1])
    nodelist_headers = parser.parse(('body', 'empty', 'endui_table'))    
    #nodelist_loop = parser.parse(('empty', 'endfor',))    
    token = parser.next_token()
    if token.contents == 'body':
        nodelist_loop = parser.parse(('empty', 'endui_table',))
        token = parser.next_token()
    
    if token.contents == 'empty':
        nodelist_empty = parser.parse(('endui_table',))
        parser.delete_first_token()
    else:
        nodelist_empty = None    

    return TableNode(loopvars, sequence, is_reversed, nodelist_headers, nodelist_loop, nodelist_empty)

#####
@register.inclusion_tag('ui_components/input.html')
def ui_input(field):    
    return {
        'field':field,        
    }

@register.inclusion_tag('ui_components/button.html')
def ui_button(url, size, icon):    
    return {
        'url':url,
        'size':size,
        'icon':icon
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

@register.filter(name='ui_row_cells')
def quit_tr(row):        
    return mark_safe(row.replace('<tr>','').replace('</tr>',''))