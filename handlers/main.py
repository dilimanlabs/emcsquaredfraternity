import os
import webapp2
import jinja2

from models import BlogPost

template_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'templates'))
#template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
    
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)
  
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class MainHandler(Handler):
    def get(self):
        self.render('new.html')
    def post(self):
        self.render('new.html', title='short title', content='long text')

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)