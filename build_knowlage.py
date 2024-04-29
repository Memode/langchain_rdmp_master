import os
from langchain.chains import RetrievalQA  # 导入 RetrievalQA 类用于检索问答
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.vectorstores import Chroma
from langchain_community.llms.chatglm3 import ChatGLM3
from langchain_community.llms import Tongyi
from langchain_openai import OpenAI,OpenAIEmbeddings

# from langchain_chatglm3 import ChatGLM3  # 自定义 ChatGLM3 类用于加载模型

# 加载embeddings
embeddings_model_dict = {
    "ernie-tiny": "nghuyong/ernie-3.0-nano-zh",
    "ernie-base": "nghuyong/ernie-3.0-base-zh",
    "text2vec": "GranymeNil/text2vec-large-chinese",
    "text2vec2": "uer/sbert-base-chinese-nil",
    "text2vec3": "E:\\workspace\\Langchain-Chatchat-master\\m3e-base",
    "bge-large-zh-v1.5":"/mnt/workspace/bge-large-zh-v1.5"
}

# 这里默认是同级目录下的 data 文件夹，将txt文件放入 data 文件夹即可
def load_document(directory="./categories"):
    loader = DirectoryLoader(directory)  # 加载文档
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=256, chunk_overlap=50)
    split_docs = text_splitter.split_documents(documents)  # 切分文档
    return split_docs


def load_embedding_mode(model_name="ernie-tiny"):
    encode_kwargs = {"normalize_embeddings": False}
    # 原始的模型参数，设置为在GPU上运行
    # model_kwargs = {"device": "cuda:0"}
    # 修改模型参数，使其在CPU上运行
    model_kwargs = {"device": "cpu"}
    return HuggingFaceEmbeddings(
        model_name=embeddings_model_dict[model_name],
        encode_kwargs=encode_kwargs,
        model_kwargs=model_kwargs
    )


def store_chroma(docs, embeddings, persist_directory='Vectorstore_KnowledgeBase'):
    # 存储 Chroma 向量化的文档
    db = Chroma.from_documents(docs, embeddings, persist_directory=persist_directory)
    db.persist()
    return db

def build_knowledge_base(directory="./categories"):
    embeddings = load_embedding_mode('text2vec3')  # 加载嵌入模型
    # embeddings = OpenAIEmbeddings()
    if not os.path.exists("Vectorstore_KnowledgeBase"):
        documents = load_document(directory)  # 加载文档
        db = store_chroma(documents, embeddings)  # 存储向量化的文档
    else:
        # 加载已存在的向量化文档
        db = Chroma(persist_directory='Vectorstore_KnowledgeBase', embedding_function=embeddings)
    # 创建 ChatGLM3 实例
    # llm = ChatGLM3(endpoint_url="http://127.0.0.1:8000/v1/chat/completions", max_token=5000)
    llm = Tongyi()
    llm.model_name="qwen-max"

    # llm = OpenAI
    retriever = db.as_retriever()  # 创建文档检索器
    knowledge_base = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type='stuff',
        retriever=retriever
    )  # 装填至 chain
    return knowledge_base

def vs_query(query):
    knowledge_base = build_knowledge_base()
    response = knowledge_base.invoke(query)  # 使用 QA 模型对问题进行推理
    return response

if __name__ == "__main__":
    print(vs_query('和渠道积分规则相关的信息'))