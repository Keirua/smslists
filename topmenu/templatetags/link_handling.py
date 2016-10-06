from django import template
from django.template.defaulttags import url, URLNode

register = template.Library()

class ActiveUrlsBuilderNode(template.Node):
	def __init__(self, url_node):
		self.url_node = url_node

	def render(self, context):
		# goal: this method automatically builds links for any template
		print 'ActiveUrlsBuilderNode context = %s' % context
		


		url = self.url_node.render(context)
		request = context['request']
		print 'url = %s' % url
		for key in range(1, 10):
			if key not in sorted(request.session['active_urls']):
				request.session['active_urls'][str(key)] = key


	# request.session['active_urls'][0] = url


	# key = request.session.get('next_template_key', '1')

	# request.session['active_urls'][key] = reverse(*args, kwargs=kwargs)
	# request.session['next_template_key'] = str(int(key)+1)

		return ''


@register.tag
def active_urls_builder(parser, token):
	url_node = url(parser, token)

	return ActiveUrlsBuilderNode(url_node)









"""
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
def active_urls_builder(parser, token):
	url_node = url(parser, token)


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
""" 