#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : executors
# @Time         : 2023/6/6 15:53
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
from meutils.decorators import backend

from jina import Document, DocumentArray, Executor, Flow, requests, Deployment
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('intfloat/multilingual-e5-base')

encode = lru_cache()(model.encode)
class E(Executor):
    @requests(on='/encode')
    def func(self, docs: DocumentArray, **kwargs):
        embeddings = encode(docs.texts, batch_size=32, normalize_embeddings=True)
        for doc, embedding in zip(docs, embeddings):
            doc.embedding = embedding

f1 = Flow(port=8501).add(uses=E)

with f1:
    # 测试
    # r = f1.post('/', DocumentArray([Document(text='我是中国人')] * 5))
    # print(r[:, 'tags'])
    # r = f1.post('/', [Document(text='我是中国人')]*5)
    # print(r.texts)

    # r = f1.post('/encode', DocumentArray([Document(text='我是中国人')] * 5))
    # print(r.texts)
    # print(r.embeddings)
    f1.block()
