"""Text converter group: markdown, plain text, and HTML sources."""
from app.converters.text_converters.md_to_docx import MarkdownToDocxConverter
from app.converters.text_converters.md_to_pdf import MarkdownToPdfConverter
from app.converters.text_converters.md_to_html import MarkdownToHtmlConverter
from app.converters.text_converters.md_to_txt import MarkdownToTxtConverter
from app.converters.text_converters.txt_to_docx import TxtToDocxConverter
from app.converters.text_converters.txt_to_pdf import TxtToPdfConverter
from app.converters.text_converters.txt_to_html import TxtToHtmlConverter
from app.converters.text_converters.html_to_pdf import HtmlToPdfConverter
from app.converters.text_converters.html_to_docx import HtmlToDocxConverter
from app.converters.text_converters.html_to_txt import HtmlToTxtConverter

TEXT_CONVERTERS = [
    MarkdownToDocxConverter,
    MarkdownToPdfConverter,
    MarkdownToHtmlConverter,
    MarkdownToTxtConverter,
    TxtToDocxConverter,
    TxtToPdfConverter,
    TxtToHtmlConverter,
    HtmlToPdfConverter,
    HtmlToDocxConverter,
    HtmlToTxtConverter,
]
