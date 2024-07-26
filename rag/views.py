from django.shortcuts import render
from django.http import JsonResponse
import os
import pickle
from langchain.llms import Ollama
from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from rag.forms import UploadFileForm

def home(request):
    form = UploadFileForm()
    return render(request, 'homev.1.0.html', {'form': form})

def setting(request):
    return render(request, 'setting.html')

def send_msg(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # Sauvegarder le fichier téléchargé
            uploaded_file = request.FILES['file']
            pdf_path = f"/tmp/{uploaded_file.name}"
            with open(pdf_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            # Initialisation du modèle
            model = Ollama(model="mistral_copy")

            # Charger le document PDF
            loader = PyMuPDFLoader(pdf_path)
            doc = loader.load()

            # Découpage du texte
            separators = ["\n\n", "\n", " ", ".", ",", "\u200b", "\uff0c", "\u3001", "\uff0e", "\u3002", ""]
            text_splitter = RecursiveCharacterTextSplitter(
                separators=separators,
                chunk_size=300,
                chunk_overlap=50,
                length_function=len,
                add_start_index=True,
            )
            chunks = text_splitter.split_documents(doc)

            # Chargement des embeddings
            emb_model = "sentence-transformers/all-MiniLM-L6-v2"
            embeddings = HuggingFaceEmbeddings(model_name=emb_model)

            EMB_CACHE_PATH = "emb_cache.pkl"
            if os.path.exists(EMB_CACHE_PATH):
                with open(EMB_CACHE_PATH, 'rb') as f:
                    cached_embeddings = pickle.load(f)
            else:
                cached_embeddings = embeddings.embed_documents([chunk.page_content for chunk in chunks])
                with open(EMB_CACHE_PATH, 'wb') as f:
                    pickle.dump(cached_embeddings, f)

            db = Chroma(persist_directory="embdb", embedding_function=embeddings)
            db.add_documents(documents=chunks)
            db.persist()

            # Traitement de la requête
            query_text = request.POST.get('query', '')
            results = db.similarity_search_with_relevance_scores(query_text, k=5)
            results.sort(key=lambda x: x[1], reverse=True)
            top_results = results[:3]

            context_text = "\n\n - -\n\n".join([doc.page_content for doc, _score in top_results])

            # Compression du prompt
            compressed_prompt = context_text[:1000]  # Limiter à 1000 caractères

            prompt_template = ChatPromptTemplate.from_template("""
            Tu t'appelles Okka.
            Tu es un assistant en intelligence artificielle conçu pour aider les utilisateurs en récupérant des informations pertinentes et en générant des réponses basées sur ces informations.
            {compressed_prompt}
            """)

            response_text = model.invoke(prompt_template.format(compressed_prompt=compressed_prompt))
            sources = [doc.metadata.get("source", None) for doc, _score in top_results]

            formatted_response = {
                "response": response_text,
                "sources": sources
            }

            return JsonResponse(formatted_response)
        else:
            return JsonResponse({"error": "Invalid form"}, status=400)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)