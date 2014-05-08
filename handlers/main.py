import os
import webapp2
import jinja2

from google.appengine.ext import ndb

class BlogPost(ndb.Model):
    title = ndb.StringProperty()
    content = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)

template_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'templates'))
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
        posts_query = BlogPost.query().order(-BlogPost.date)
        posts = posts_query.fetch(10)
        self.render('new.html', posts=posts)

    def post(self):
        post = BlogPost()
        post.title = self.request.get('title')
        post.content = self.request.get('content')
        post.put()
        self.redirect('/')

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)