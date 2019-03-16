# -*- code:utf-8 -*-
from flask import Flask,render_template
from livereload import Server
from functools import reduce

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', title="<h1>Welcome</h1>", body="## header2")



@app.template_filter('md')
def markdown_to_html(txt):
    from markdown import markdown
    return markdown(txt)


def read_md(filename):
    with open(filename) as md_file:
        content = reduce(lambda x,y:x+y,md_file.readlines( ))
    return content

@app.context_processor
def inject_methods():
    return dict(read_md = read_md)

if __name__ == '__main__':
    live_sever = Server(app.wsgi_app)
    live_sever.watch('**/*.*')
    live_sever.serve(open_url=True)
    #app.run(debug=True)  #debug 参数