import os

from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings

TEXT_FILE = "tmp/imdb_titles_overview.txt"
VECTOR_DATABASE = f"{TEXT_FILE}.vector.db"

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

if not os.path.exists(VECTOR_DATABASE):

    texts = None
    with open(TEXT_FILE, 'r', encoding='latin-1') as f:
        texts = f.readlines()        

    texts = [t.strip('\n') for t in texts]

    print(f'len texts: {len(texts)}')

    vector_db = FAISS.from_texts(texts, embeddings)

    vector_db.save_local(VECTOR_DATABASE)

vector_db = FAISS.load_local(VECTOR_DATABASE, embeddings, allow_dangerous_deserialization=True)

the_continue = True
while the_continue:
    query = input("Digite a query: ")

    if query in ["exit", "sair",'quit']:
        the_continue = False
        continue

    resultados = vector_db.similarity_search(query, k=5)

    print(f'len result: {len(resultados)}')
    for i, r in enumerate(resultados):
        print('_'*100)
        print(f"{i+1}: {r.page_content}")
