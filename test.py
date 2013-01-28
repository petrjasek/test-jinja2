import unittest
from jinja2 import Template, nodes, Environment
from jinja2.ext import Extension

class ListArticlesExtension(Extension):
    tags = {'list_articles'}

    def __init__(self, environment):
        super(ListArticlesExtension, self).__init__(environment)

    def parse(self, parser):
        parser.stream.skip()
        body = parser.parse_statements(['name:end_list_articles'], drop_needle=True)
        target = nodes.Name('article', 'store', lineno=1)
        iter = nodes.List([nodes.Const('tic'), nodes.Const('toc')], lineno=1)
        return nodes.For(target, iter, body, [], None, None, lineno=1)

class TestListArticles(unittest.TestCase):

    def test_list_articles(self):
        env = Environment(extensions=[ListArticlesExtension])
        template = env.from_string('<ul>{% list_articles %}<li>{{ article }}</li>{% end_list_articles %}</ul>')
        self.assertEqual('<ul><li>tic</li><li>toc</li></ul>', template.render())

if __name__ == '__main__':
    unittest.main()
