from bs4 import BeautifulSoup
import urllib.request
import re
import os

def makePdflist(soup):
    href_list = []
    for link in soup.find_all('a'):
        href_list.append(link.get('href'))
    new_href_list = [i for i in href_list if i is not None] #去除None
    pdf_list = ['https://arxiv.org' + s for s in new_href_list if '/pdf' in s]
    return pdf_list

if __name__ == "__main__":
    path = './cs.AI/'
    path_list = os.listdir(path)
    for t in path_list:
        file_name = path + t
        with open(file_name) as html:
            soup = BeautifulSoup(html, 'html.parser')
        pdf_list = makePdflist(soup)
        html.close()
        with open("arxiv_paper_list.txt",  "w") as f:
            f.writelines(s + '\n' for s in pdf_list)
    