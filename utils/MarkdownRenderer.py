import re
import mistune

class MarkdownRenderer:
    def __init__(self):
        self.renderer = CustomRenderer()
        self.markdown = mistune.Markdown(renderer=self.renderer)

    def render(self, content):
        return self.markdown(content)

class CustomRenderer(mistune.HTMLRenderer):
    def paragraph(self, text):
        # 添加高亮背景
        pattern = r'\[highlight\](.*?)\[/highlight\]'
        replacement = r'<span class="highlight">\1</span>'
        text = re.sub(pattern, replacement, text)
        # 添加背景线
        pattern = r'\[bgline\](.*?)\[/bgline\]'
        replacement = r'<span class="bgline">\1</span>'
        text = re.sub(pattern, replacement, text)
        # 添加下划背景线
        pattern = r'\[underline\](.*?)\[/underline\]'
        replacement = r'<span class="underline">\1</span>'
        text = re.sub(pattern, replacement, text)
        # 添加success框
        pattern = r'\[success\](.*?)\[/success\]'
        replacement = r'<article class="message is-success"><div class="message-body"><p>\1</p></div></article>'
        text = re.sub(pattern, replacement, text)
        # 添加info框
        pattern = r'\[info\](.*?)\[/info\]'
        replacement = r'<article class="message is-info"><div class="message-body"><p>\1</p></div></article>'
        text = re.sub(pattern, replacement, text)
        # 添加warning框
        pattern = r'\[warning\](.*?)\[/warning\]'
        replacement = r'<article class="message is-warning"><div class="message-body"><p>\1</p></div></article>'
        text = re.sub(pattern, replacement, text)
        # 添加自定义文字颜色与文字大小
        pattern = r'\[font\s+color=(.*?)\s*(?:size=(\d+))?\](.*?)\[/font\]'
        replacement = r'<span style="color:\1; font-size:\2px;">\3</span>'
        text = re.sub(pattern, replacement, text)

        return super().paragraph(text)

    # 将文章中的图片支持点击放大
    def image(self, alt, url, title=None):
        title_attr = ' title="{}"'.format(title) if title else ""
        return '<img src="{}" alt="{}"{} class="image-zoomableqwq">'.format(url, alt, title_attr)

# 使用示例
# renderer = MarkdownRenderer()
# comic_intro = "这是一个[highlight]高亮文本[/highlight]的例子。"
# html = renderer.render(comic_intro)
# print(html)