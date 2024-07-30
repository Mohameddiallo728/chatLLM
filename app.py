import os
import streamlit as st
from streamlit_chat import message
from langchain_community.llms import Ollama
from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
import pickle

# Define paths
CHROMA_PATH = "embdb"
EMB_CACHE_PATH = "emb_cache.pkl"
emb_model = "sentence-transformers/all-MiniLM-L6-v2"

# App title
st.set_page_config(page_title="RAG mistral")
with st.sidebar:
    st.title("RAG mistral")

# Store LLM-generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "Comment puis-je vous aider aujourd'hui ?"}]

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "Comment puis-je vous aider aujourd'hui ?"}]
st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

# Sidebar for PDF upload
uploaded_file = st.sidebar.file_uploader("Choisissez un fichier PDF", type="pdf")

if uploaded_file:
    pdf_bytes = uploaded_file.read()
    pdf_path = os.path.join("uploads", uploaded_file.name)
    
    # Create uploads directory if not exists
    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
    
    with open(pdf_path, "wb") as f:
        f.write(pdf_bytes)

    # Process the PDF
    loader = PyMuPDFLoader(pdf_path)
    doc = loader.load()

    # Text splitting
    separators = ["\n\n", "\n", " ", ".", ",", "\u200b", "\uff0c", "\u3001", "\uff0e", "\u3002", ""]
    text_splitter = RecursiveCharacterTextSplitter(
        separators=separators,
        chunk_size=300,
        chunk_overlap=50,
        length_function=len,
        add_start_index=True,
    )

    chunks = text_splitter.split_documents(doc)
    st.sidebar.success(f"PDF chargé et découpé en {len(chunks)} chunks.")

    # Embeddings
    embeddings = HuggingFaceEmbeddings(model_name=emb_model)

    # Cache embeddings
    if os.path.exists(EMB_CACHE_PATH):
        with open(EMB_CACHE_PATH, 'rb') as f:
            cached_embeddings = pickle.load(f)
    else:
        cached_embeddings = embeddings.embed_documents([chunk.page_content for chunk in chunks])
        with open(EMB_CACHE_PATH, 'wb') as f:
            pickle.dump(cached_embeddings, f)

    # Create Chroma database
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)
    db.add_documents(documents=chunks)
    db.persist()
    st.sidebar.success("Embeddings créés et persistés.")

    # Initialize model
    model = Ollama(model="mistral_copy")

# Display chat messages
st.header("Conversation")
for i, msg in enumerate(st.session_state.messages):
    is_user = msg["role"] == "user"
    avatar = "lorelei/svg?seed=Aneka" if is_user else "bottts/svg?seed=Aneka"
    message(msg["content"], is_user=is_user, key=str(i), avatar_style=avatar)

# Define prompt template
PROMPT_TEMPLATE = """
Tu t'appelles Okka.
Tu es un assistant en intelligence artificielle conçu pour aider les utilisateurs en récupérant des informations pertinentes et en générant des réponses basées sur ces informations. 
Ton objectif est de fournir des réponses claires et utiles.

L'utilisateur a posé la question suivante : "{question}"
Recherche des documents pertinents dans la base de connaissances et utilise ces informations pour répondre à la question.

Réponds à la question en utilisant uniquement le contexte suivant :
{context}
- -
Réponds à la question ci-dessous en te basant uniquement sur le contexte fourni, dans la même langue que la question :
Question : {question}
"""

# User-provided prompt
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    message(prompt, is_user=True, key=f"user_{len(st.session_state.messages)}", avatar_style="lorelei/svg?seed=Aneka")

    # Generate a new response if the last message is not from the assistant
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.spinner('La réponse est en cours de génération...'):
            results = db.similarity_search_with_relevance_scores(prompt, k=3)
            context_text = "\n\n - -\n\n".join([doc.page_content for doc, _score in results])
            prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
            formatted_prompt = prompt_template.format(context=context_text, question=prompt)

            response = model.invoke(formatted_prompt)

            message_data = {"role": "assistant", "content": response}
            st.session_state.messages.append(message_data)
            message(response, is_user=False, key=f"assistant_{len(st.session_state.messages)}", avatar_style="bottts/svg?seed=Aneka")
