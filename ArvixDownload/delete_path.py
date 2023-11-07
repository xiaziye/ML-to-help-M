import os

file_path = "G:/CV_conference_paper_download-main/arxiv/arxiv_paper_list.txt" #todo1
download_path = "G:/CV_conference_paper_download-main/arxiv/article_Project" #todo2

path_list = os.listdir(download_path)
pdf_list = [s.replace('.pdf','') for s in path_list]
pdf_dlist = ['https://arxiv.org/pdf/' + s+'\n' for s in pdf_list ]
with open(file_path, 'r') as f:
    pdf_olist=f.readlines()
    #print(pdf_olist)
    pdf_nlist = [i for i in pdf_olist if i not in pdf_dlist]
    #print(pdf_nlist)
    f.close()
with open(file_path, 'w+') as f:
    f.writelines(s  for s in pdf_nlist)
    f.close()