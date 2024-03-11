import urllib.request
 
def getHtml(url):
    html = urllib.request.urlopen(url).read()
    return html
 
def saveHtml(file_name, file_content):
    #    注意windows文件命名的禁用符，比如 /
    with open("./cs.AI/" + file_name.replace('/', '_') + ".html", "wb") as f:
        #   写文件用bytes而不是str，所以要转码
        f.write(file_content)

aurl = "https://arxiv.org/list/cs.AI/recent"
html = getHtml(aurl)
saveHtml("cs.AI.0", html)

for i in range(1, 15):
    ii = i * 25
    aurl = ("https://arxiv.org/list/cs.AI/pastweek?skip=%d&show=%d.html" %(ii, ii))
    name = ("cs.AI.%d" %i)
    html = getHtml(aurl)
    saveHtml(name, html)
 
print("下载成功")