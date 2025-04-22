from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Document
from .task import run_document_processing
from rich import print
from core.ai.chromadb import chroma, openai_ef

class DocumentUploadView(View):
    template_name='documents/index.html'

    def get(self, request):
        return render(request, template_name=self.template_name)
    
    def post(self, request):
        file = request.FILES.get("file")

        try:
            document = Document.objects.create(file=file, name=file.name)
            run_document_processing(document)

            return redirect('documents')
        
        except Exception as e:
            print(e)
            messages.error(request, f"Error uploading document: {str(e)}")

            return render(request, self.template_name)

    
class QueryView(View):
    template_name = 'documents/query.html'
    pk_url_kwarg = 'id'

    def get_object(self):
        return get_object_or_404(Document, pk=self.kwargs.get(self.pk_url_kwarg))

    def get(self, request, *args, **kwargs):
        delivery = self.get_object()
        return render(request, self.template_name, context={"delivery": delivery})
    
    def post(self, request, *args, **kwargs):
        delivery = self.get_object()
        collection_name = delivery.id

        print("collection name:", collection_name)

        query = request.POST.get("query")

        collection = chroma.get_collection(name=collection_name, embedding_function=openai_ef)
        result = collection.query(
            query_texts=[query],
            n_results=3,
        )

        print(result)

        return redirect('query', id=delivery.id)