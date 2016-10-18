import re

from django import template
from django.template.base import Token
from django.template.defaulttags import url, URLNode

register = template.Library()

LINK_RX = re.compile(r'\d+')
QUERY_PARAM_SEPARATOR = '?'

class ActiveUrlsBuilderNode(template.Node):

	def __init__(self, url_node, link_id=None, query_params=[]):
		self.url_node = url_node
		self.link_id = link_id
		self.query_params = query_params

	def render(self, context):
		print 'ActiveUrlsBuilderNode context = %s' % context

		url = self.url_node.render(context) + '' if not self.query_params else '?%s' % '&'.join(self.query_params)
		request = context['request']
		print 'url = %s' % url

		key = self.link_id or str(int(max(request.session['active_urls'].keys()[:5] or [0]))+1)
		print 'active urls = %s' % request.session['active_urls']
		request.session['active_urls'][key] = url

		return key

@register.tag
def active_urls_builder(parser, token):

	link_id = None
	query_params = []

	bits = token.split_contents()

	if LINK_RX.match(bits[1]):
		link_id = bits[1]
		bits = [bits[0]]+bits[2:]

	if QUERY_PARAM_SEPARATOR in bits:
		query_params_start = bits.index(QUERY_PARAM_SEPARATOR)
		query_params = bits[query_params_start + 1:]
		bits = bits[:query_params_start]

	url_node = url(parser, Token(token.token_type, ' '.join(bits), token.position, token.lineno))

	return ActiveUrlsBuilderNode(url_node, link_id, query_params)
