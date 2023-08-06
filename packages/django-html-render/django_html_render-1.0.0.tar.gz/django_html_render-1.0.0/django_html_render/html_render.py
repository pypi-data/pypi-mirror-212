from django.utils.html import format_html


class HtmlRender:

    @staticmethod
    def p(text, color):
        return format_html('<p style="color:{}; padding-left: 0px; margin-top: 0px">{}</p>'.format(color, text))

    @staticmethod
    def br():
        return format_html('<br/>')

    @staticmethod
    def html(htm):
        return format_html(htm)
