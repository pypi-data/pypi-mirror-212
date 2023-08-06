from django.utils.html import format_html


class RenderImage:
    width = 100
    height = 100

    def __init__(self, width=None, height=None, *arg, **kw):
        if width:
            self.width = width
        if height:
            self.height = height

    def html_image(self, url):
        width = 'width="{}px"'.format(self.width)
        height = 'height="{}px"'.format(self.height)
        style = 'style="display: block; object-fit: cover"'
        return '<img src={} {} {} {} />'.format(url, width, height, style)

    def render(self, url):
        # pass all self into method
        return format_html(self.html_image(url))
