import urllib.request
from .core.parser import Parser
from .core.html import HtmlNode

def parse(data:str) -> list[HtmlNode]:
    '''
    Parses html data and returns a collection of root nodes.
    '''
    return Parser().parse(data)

def get(url:str, encoding:str = 'latin-1'):
    '''
    Basic http get request.
    '''
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    return response.read().decode(encoding)