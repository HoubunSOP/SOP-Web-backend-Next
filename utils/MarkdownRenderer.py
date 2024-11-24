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
        # 添加文字居中
        pattern = r'\[center\](.*?)\[/center\]'
        replacement = r'<p class="text-center">\1</p>'
        text = re.sub(pattern, replacement, text)
        # 添加文字居中
        pattern = r'\[right\](.*?)\[/right\]'
        replacement = r'<p style="text-align: center;">\1</p>'
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
        pattern = r'\[font\s+color=(.*?)\s*(?:size=(.*?))?\](.*?)\[/font\]'
        replacement = r'<font color="\1" size="\2">\3</font>'
        replaced_text = re.sub(pattern, replacement, text)

        return super().paragraph(replaced_text)

# 使用示例
# renderer = MarkdownRenderer()
# comic_intro = "这是一个[highlight]高亮文本[/highlight]的例子。"
# html = renderer.render(comic_intro)
# print(html)
