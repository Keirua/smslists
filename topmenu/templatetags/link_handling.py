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

		key = max(request.session['active_urls'].keys()[:5] or [0])+1
		print 'active urls = %s' % request.session['active_urls']
		request.session['active_urls'][key] = url
				
	# request.session['active_urls'][0] = url
	# key = request.session.get('next_template_key', '1')
	# request.session['active_urls'][key] = reverse(*args, kwargs=kwargs)
	# request.session['next_template_key'] = str(int(key)+1)

		return str(key)

@register.tag
def active_urls_builder(parser, token):
	url_node = url(parser, token)

	return ActiveUrlsBuilderNode(url_node)