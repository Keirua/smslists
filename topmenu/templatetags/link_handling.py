from django import template

register = template.Library()

class ActiveUrlsBuilderNode(template.Node):
	def __init__(self, date_to_be_formatted, format_string):
	    self.category = template.Variable(category)
	    self.listing_id = template.Variable(listing_id)

	def render(self, context):
	    try:
	    	category_value = self.category.resolve(context)
	    	listing_id_value = self.listing_id.resolve(context)
	        return ''
	    except template.VariableDoesNotExist:
	        return ''

@register.tag
def active_urls_builder(request, *args, **kwargs):
	key = request.session.get('next_template_key', '1')

	request.session['active_urls'][key] = reverse(*args, kwargs=kwargs)
	request.session['next_template_key'] = str(int(key)+1)

	return key

@register.tag
def custom_compilation(parser, token):
	try:
		tag_name, reverse_lookup, category, listing_id = token.split_contents()
	except ValueError:
		raise template.TemplateSyntaxError(
			"%r tag requires a single argument" % token.contents.split()[0]
		)
	if not (format_string[0] == format_string[-1] and format_string[0] in ('"', "'")):
		raise template.TemplateSyntaxError(
			"%r tag's argument should be in quotes" % tag_name
			)
	return ActiveURlsBuilderNode(category, listing_id)