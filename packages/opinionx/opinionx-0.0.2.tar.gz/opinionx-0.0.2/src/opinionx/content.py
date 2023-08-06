from trafilatura import bare_extraction
import hashlib

def quick_content(html_text):
    content = bare_extraction(html_text)
    if content==None:
        return ""
    text = content["text"]
    return text

def get_md5_str(text):
    unique_id = hashlib.md5(text.encode())
    page_id = str(unique_id.hexdigest())
    return page_id