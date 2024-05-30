import streamlit as st
import os
from llama_index.vector_stores.faiss import FaissVectorStore
from llama_index.core import load_index_from_storage, StorageContext
from llama_index.core.storage.docstore import SimpleDocumentStore
from llama_index.core.storage.index_store import SimpleIndexStore
from openai import OpenAI

# Ensure that st.set_page_config is the first Streamlit command
st.set_page_config(layout="wide")

client = OpenAI(api_key = st.secrets['OPENAI_API_KEY'])
os.environ['OPENAI_API_KEY'] = st.secrets['OPENAI_API_KEY']


@st.cache_resource
def create_retriever(top_k):
    index = load_index_from_storage(storage_context=StorageContext.from_defaults(
        docstore=SimpleDocumentStore.from_persist_dir(persist_dir="storage"),
        vector_store=FaissVectorStore.from_persist_dir(persist_dir="storage"),
        index_store=SimpleIndexStore.from_persist_dir(persist_dir="storage"),
    ))
    return index.as_retriever(retriever_mode='embedding', similarity_top_k=int(top_k))

st.title('Policy Times Knowledgebase Semantic Search')

query = st.text_input(label='Please enter your query - ', value='')
top_k = st.number_input(label='Top k - ', min_value=3, max_value=5, value=3)

retriever = create_retriever(top_k)

if query and top_k:
    col1, col2 = st.columns([3, 2])
    with col1:
        response = []
        for i in retriever.retrieve(query):
            response.append({
                'name': i.metadata.get('name', 'Unknown'),
                'link': i.metadata.get('link', 'No link provided'),
                'date': i.metadata.get('date', 'No date provided'),
                'content': i.get_text(),
            })
        st.json(response)

    with col2:
        summary = st.empty()
        top3 = []
        top3_name = []
        for i in response[:3]:  # Limit to top 3 responses
            top3.append(i["content"])
            top3_name.append(i["name"])

        # Prepare the structured answer
        temp_summary = []
        key_counter = 0  # Counter for generating unique keys
        for resp in client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": f"Act as a Policy Expert and Information Specialist for the Policy Times Chamber of Commerce. Your primary responsibility is to provide accurate, relevant, and timely information to users based on the organization's comprehensive knowledgebase. Now answer the {query}, using the following knowledgebase: {top3}. Your knowledgebase also contains name of the document, give it when answering so as to making your answer clear: {top3_name}. Strictly answer based on the available knowledge base."},
                {"role": "user", "content": f"""Summarize the following interpretation of documents in context of the query '{query}':

{top3_name[2]}
Summary:
{top3[2]}

{top3_name[1]}
Summary:
{top3[1]}

{top3_name[0]}
Summary:
{top3[0]}"""},
            ],
            stream=True):
            if resp.choices[0].finish_reason == "stop":
                break
            temp_summary.append(resp.choices[0].delta.content)
            result = "".join(temp_summary).strip()

            # Update the summary in real-time
            summary.text_area(label="Response", value=result, height=750, max_chars=None, key=f"response_text_area_{key_counter}")
            key_counter += 1  # Increment key counter to ensure uniqueness








# import streamlit as st
# import os
# from llama_index.vector_stores.faiss import FaissVectorStore
# from llama_index.core import load_index_from_storage, StorageContext
# from llama_index.core.storage.docstore import SimpleDocumentStore
# from llama_index.core.storage.index_store import SimpleIndexStore
# from openai import OpenAI

# # Ensure that st.set_page_config is the first Streamlit command
# st.set_page_config(layout="wide")

# @st.cache_resource
# def create_retriever():
#     index = load_index_from_storage(storage_context=StorageContext.from_defaults(
#         docstore=SimpleDocumentStore.from_persist_dir(persist_dir="storage"),
#         vector_store=FaissVectorStore.from_persist_dir(persist_dir="storage"),
#         index_store=SimpleIndexStore.from_persist_dir(persist_dir="storage"),
#     ))
#     return index.as_retriever(retriever_mode='embedding', similarity_top_k=int(top_k))

# st.title('Policy Times Knowledgebase Semantic Search')

# query = st.text_input(label='Please enter your query - ', value='')
# top_k = st.number_input(label='Top k - ', min_value=3, max_value=5, value=3)

# retriever = create_retriever()

# if query and top_k:
#     col1, col2 = st.columns([3, 2])
#     with col1:
#         response = []
#         for i in retriever.retrieve(query):
#             response.append({
#                 'name': i.metadata.get('name', 'Unknown'),
#                 'link': i.metadata.get('link', 'No link provided'),
#                 'date': i.metadata.get('date', 'No date provided'),
#                 'content': i.get_text(),
#             })
#         st.json(response)

#     with col2:
#         summary = st.empty()
#         top3 = []
#         top3_name = []
#         for i in response[:3]:  # Limit to top 3 responses
#             top3.append(i["content"])
#             top3_name.append(i["name"])
        
#         # # Prepare thinking process
#         # thinking_process = f"""
#         # <thinking>
#         # User query: {query}
#         # Retrieved documents: {', '.join(top3_name)}
#         # Content analyzed: {', '.join(top3)}
#         # </thinking>
#         # """
        
#         # st.markdown(thinking_process)
        
#         # Prepare the structured answer
#         temp_summary = []
#         for resp in client.chat.completions.create(
#             model="gpt-4-1106-preview",
#             messages=[
#                 {"role": "system", "content": f"Act as a Policy Expert and Information Specialist for the Policy Times Chamber of Commerce. Your primary responsibility is to provide accurate, relevant, and timely information to users based on the organization's comprehensive knowledgebase. Now answer the {query}, using the following knowledgebase: {top3}. Your knowledgebase also contains name of the document, give it when answering so as to making your answer clear: {top3_name}. Strictly answer based on the available knowledge base."},
#                 {"role": "user", "content": f"""Summarize the following interpretation of documents in context of the query '{query}':

# {top3_name[2]}
# Summary:
# {top3[2]}

# {top3_name[1]}
# Summary:
# {top3[1]}

# {top3_name[0]}
# Summary:
# {top3[0]}"""},
#             ],
#             stream=True):
#             if resp.choices[0].finish_reason == "stop":
#                 break
#             temp_summary.append(resp.choices[0].delta.content)
#             result = "".join(temp_summary).strip()
        
#         answer = f"""
#         {result}
#         """
        
#         summary.markdown(answer)





















# import streamlit as st
# import os
# from llama_index.vector_stores.faiss import FaissVectorStore
# from llama_index.core import load_index_from_storage, StorageContext
# from llama_index.core.storage.docstore import SimpleDocumentStore
# from llama_index.core.storage.index_store import SimpleIndexStore
# from openai import OpenAI

# st.set_page_config(layout = "wide")

# # client = OpenAI(api_key = st.secrets['OPENAI_API_KEY'])
# # os.environ['OPENAI_API_KEY'] = st.secrets['OPENAI_API_KEY']



# @st.cache_resource
# def create_retriever():
#     index = load_index_from_storage(storage_context = StorageContext.from_defaults(
#                 docstore = SimpleDocumentStore.from_persist_dir(persist_dir = "storage"),
#                 vector_store = FaissVectorStore.from_persist_dir(persist_dir = "storage"),
#                 index_store = SimpleIndexStore.from_persist_dir(persist_dir = "storage"),
#             ))
#     return index.as_retriever(retriever_mode = 'embedding', similarity_top_k = int(top_k))

# st.title('Crop Data Semantic Search')

# query = st.text_input(label = 'Please enter your query - ', value = '')
# top_k = st.number_input(label = 'Top k - ', min_value = 3, max_value = 5, value = 3)

# retriever = create_retriever()

# if query and top_k:
#     col1, col2 = st.columns([3, 2])
#     with col1:
#         response = []
#         for i in retriever.retrieve(query):
#             response.append({
#                     'Document' : i.metadata['link'][40:-4],
#                     'Source' : i.metadata['link'],
#                     'Text' : i.get_text(),
#                     'Score' : i.get_score(),
#                 })
#         st.json(response)

#     with col2:
#         summary = st.empty()
#         top3 = []
#         top3_couplet = []
#         top3_name = []
#         for i in response:
#              top3.append(i["Text"])
#              top3_name.append(i["Document"])
#         temp_summary = []
#         for resp in client.chat.completions.create(model = "gpt-4-1106-preview",
#             messages = [
#                     {"role": "system", "content": f"Act as a query answering GPT for The Ministry of Agriculture and Farmers Welfare, India. You answer queries of officers and farmers using your knowledgebase. Now answer the {query}, using the following knowledgebase:{top3} Your knowledgebase also contains name of the document, give it when answering so as to making your answer clear: {top3_name}. Strictly answer based on the available knowledge base."},
#                     {"role": "user", "content": f"""Summarize the following interpretation of couplets in context of the query “{query}”:

# {top3_name[2]}
# Summary:
# {top3[2]}

# {top3_name[1]}
# Summary:
# {top3[1]}

# {top3_name[0]}
# Summary:
# {top3[0]}"""},
#                 ],
#             stream = True):
#                 if resp.choices[0].finish_reason == "stop":
#                     break
#                 temp_summary.append(resp.choices[0].delta.content)
#                 result = "".join(temp_summary).strip()
#                 summary.markdown(f'{result}')
