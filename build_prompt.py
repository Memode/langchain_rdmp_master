import os
import glob

import chromadb
from chromadb import Documents, EmbeddingFunction, Embeddings
# from chromadb.utils.embedding_functions import (
#     SentenceTransformerEmbeddingFunction
# )
from transformers import AutoTokenizer, AutoModel
import torch


class MyEmbeddingFunction(EmbeddingFunction):
    def __init__(self, model_name, device="cpu") -> None:
        self.model_name = model_name
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)
        self.device = torch.device(device)
        self.model.to(self.device)

    @staticmethod
    def mean_pooling(model_output, attention_mask):
        token_embeddings = model_output[0]  # First element of model_output contains all token embeddings
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)

    def __call__(self, input: Documents) -> Embeddings:
        encoded_input = self.tokenizer(list(input), padding=True, truncation=True, return_tensors='pt').to(self.device)
        # print(encoded_input)
        with torch.no_grad():
            model_output = self.model(**encoded_input)
        if "bge" in self.model_name.lower():
            sentence_embeddings = model_output[0][:, 0]
        else:
            sentence_embeddings = self.mean_pooling(model_output, encoded_input['attention_mask'])
        sentence_embeddings = torch.nn.functional.normalize(sentence_embeddings, p=2, dim=1)
        return sentence_embeddings.cpu().numpy().tolist()


class PromptMessage():
    def __init__(self) -> None:
        # 数据库路径
        self.dbpath = "./VectorStore_prompt"
        # 数据文件路径
        self.source_directory = "./data"
        # 文件后缀
        self.file_ext = '*.txt'

        if not os.path.exists(self.dbpath):
            self.client = chromadb.PersistentClient(path=self.dbpath)
            self.collection = self.client.get_or_create_collection(
                name="prompt_info",
                # metadata={"hnsw:space": "cosine"},
                # embedding_function=MyEmbeddingFunction(model_name="E:\\workspace\\Langchain-Chatchat-master\\m3e-base", device="cpu")
            )

            # 初始化数据
            # 打开文件
            files = glob.glob(os.path.join(self.source_directory, self.file_ext))

            index = 0
            for file_name in files:
                with open(file_name, 'r', encoding='utf-8') as file:
                    # 逐行读取文件
                    for line in file:
                        # 打印每行内容
                        line = line.strip()
                        values = line.split(":")
                        # 检查行是否为空
                        if len(values)>=2:
                            index = index + 1
                            self.collection.add(
                                documents=[values[1]],
                                metadatas=[{"type": values[0]}],
                                ids=[str(index)])

        else:
            self.client = chromadb.PersistentClient(path="./VectorStore_prompt")
            self.collection = self.client.get_or_create_collection(
                name="prompt_info",
                # metadata={"hnsw:space": "cosine"},
                # embedding_function=MyEmbeddingFunction(model_name="E:\\workspace\\Langchain-Chatchat-master\\m3e-base", device="cpu")
            )


    def delDB(self):
        self.client.delete_collection(name="prompt_info")

    # 添加文档
    def load_data(self):
        # 打开文件
        files = glob.glob(os.path.join(self.source_directory, self.file_ext))

        index = 0
        for file_name in files:
            with open(file_name, 'r', encoding='utf-8') as file:
                # 逐行读取文件
                for line in file:
                    # 打印每行内容
                    line = line.strip()
                    values = line.split(":")
                    if len(values)>=2:
                        index = index + 1
                        self.collection.add(
                            documents=[values[1]],
                            metadatas=[{"type": values[0]}],
                            ids=[str(index)])




    # 检索相似性文档
    def query_prompt(self, message):
        resp = self.collection.query(
            # query_embeddings=[[1,2,3]],
            query_texts=[message],
            n_results=3
            # where={"author": {"$eq": "john"}}, # 表示 metadata 中 "author" 字段值等于 "jack" 的文档
            # where_document={"$contains": message}, # 表示文本内容中包含 "john" 的文档.
        )
        # print(resp)
        return resp

if __name__ == "__main__":
    prom = PromptMessage()
    # prom.delDB()
    # print(prom)
    # print(prom.load_data())
    # print(prom.collection.peek())
    prm = prom.query_prompt("主套餐政策规则积分")

    print(prm["documents"][0])