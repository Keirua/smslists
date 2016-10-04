from django import template

register = template.Library()

class TestyNode(template.Node):
	def __init__(self):
		pass
	def render(self):
		pass

@register.tag
def custom_compilation(parser, token):
	try:
		tag_name, format_string = token.split_contents()
	except ValueError:
		raise template.TemplateSyntaxError(
			"%r tag requires a single argument" % token.contents.split()[0]
		)
	if not (format_string[0] == format_string[-1] and format_string[0] in ('"', "'")):
		raise template.TemplateSyntaxError(
			"%r tag's argument should be in quotes" % tag_name
			)
	return TestyNode()

@register.tag
def testy(*args, **kwargs):
	print 'link_handling loaded!'

