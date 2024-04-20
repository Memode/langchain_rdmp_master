# import
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from langchain_community.embeddings import HuggingFaceEmbeddings 
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders.text import TextLoader
# from langchain_community.document_loaders import DirectoryLoader

import glob
import os

# 数据库路径
db_dir = "./VectorStore"
# 文档路径
source_directory = "./data"
# 文件后缀
file_ext = '*.txt'

# create the open-source embedding function
# embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
# 使用中文嵌入层编码器
ebd_function = HuggingFaceEmbeddings(model_name="E:\\workspace\\Langchain-Chatchat-master\\m3e-base")

def add_files_to_db(filepath:str="",file_ext:str=""):
    docx_files = glob.glob(os.path.join(source_directory, file_ext))
    text_list=[]
    for file_name in docx_files:
        print(file_name)
        loader = TextLoader(file_name)
        documents = loader.load()
        text_list.extend(documents)

    # split it into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = text_splitter.split_documents(text_list)

    # load it into Chroma
    db = Chroma.from_documents(docs, ebd_function, persist_directory=db_dir)
    # save db to disk
    db.persist()


def query_db(db:Chroma,query:str=""):

    # query it
    docs = db.similarity_search(query)

    # print results
    print(docs[0].page_content)
    print("-----------------------------------------")


    
 
if __name__=="__main__":

    # 只需执行一次
    add_files_to_db(source_directory,file_ext)

    db = Chroma(persist_directory=db_dir,embedding_function=ebd_function)
    query = "怎么治疗骨质疏松症?"
    query_db(db,query)
    query = "什么是渠道结算?"
    query_db(db,query)
    db = None
    pass