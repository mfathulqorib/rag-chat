from django.shortcuts import render, redirect
from django.views import View
from .models import Document
from .task import process_document
from rich import print
from core.ai.chromadb import chroma, openai_ef

class DocumentUploadView(View):
    def get(self, request):
        return render(request, template_name='documents/index.html')
    
    def post(self, request):
        file = request.FILES.get("file")

        try:
            document = Document.objects.create(file=file, name=file.name)
            process_document(document)

        except Exception as e:
            print(e)

        return redirect('documents')
    
class QueryView(View):
    def get(self, request):
        return render(request, template_name='documents/query.html')
    
    def post(self, request):
        query = request.POST.get("query")

        collection = chroma.get_collection(name="6807110bd2aa9f74e5d3bc33", embedding_function=openai_ef)
        result = collection.query(
            query_texts=[query],
            n_results=3,
        )

        print(result)
        
        return redirect('query')