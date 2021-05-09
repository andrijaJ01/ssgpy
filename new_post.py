title=input('enter title: ')
subtitle=input('enter subtitle: ')
summary=input('enter summary: ')
slug=input('enter slug: ')
imgname=input('enter image(just name no extension needed,should be jpg): ')
image=f"assets/img/{imgname}.jpg"
author=input('enter author: ')
date=input('enter date: ')


outfile=f'content/{slug}.md'

template=f"---\ntitle: {title}\nsubtitle: {subtitle}\nsummary: {summary}\nslug: {slug}\nimg: {image}\nauthor: {author}\ndate: {date}\n---\n__delete this and put content__"


with open(outfile,'w') as f:
    f.write(template)
print('content written')
print('now run main.py to generate the html file')    
