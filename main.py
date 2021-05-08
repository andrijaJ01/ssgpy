
import os
from datetime import datetime
from jinja2 import Environment, PackageLoader
from markdown2 import markdown


POSTS = {}

for markdown_post in os.listdir('content'):
    file_path = os.path.join('content', markdown_post)

    with open(file_path, 'r') as file:
        POSTS[markdown_post] = markdown(file.read(), extras=['metadata'])

    
POSTS = {
    post: POSTS[post] for post in sorted(POSTS, key=lambda post: datetime.strptime(POSTS[post].metadata['date'], '%Y-%m-%d'), reverse=True)
}

env = Environment(loader=PackageLoader('main', 'templates'))
home_template = env.get_template('index.html')
post_template = env.get_template('post.html')
about_template = env.get_template('about.html')
contact_template = env.get_template('contact.html')


posts_metadata = [POSTS[post].metadata for post in POSTS]
home_html = home_template.render(posts=posts_metadata)
about_html = about_template.render()
contact_html = contact_template.render()


with open('output/index.html', 'w') as file:
    file.write(home_html)

with open('output/about.html', 'w') as file:
    file.write(about_html)

with open('output/contact.html', 'w') as file:
    file.write(contact_html)


for post in POSTS:
    post_metadata = POSTS[post].metadata

    post_data = {
        'content': POSTS[post],
        'title': post_metadata['title'],
        'subtitle': post_metadata['subtitle'],
        'author':post_metadata['author'],
        'date': post_metadata['date'],
    }

    post_html = post_template.render(post=post_data)
    post_file_path = 'output/posts/{slug}.html'.format(slug=post_metadata['slug'])
    print(f"Written: {post_file_path}")
    os.makedirs(os.path.dirname(post_file_path), exist_ok=True)
    with open(post_file_path, 'w') as file:
        file.write(post_html)
