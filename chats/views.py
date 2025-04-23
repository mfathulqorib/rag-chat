from django.views.generic import View
from django.shortcuts import render
from core.utils import generate_id


class ChatView(View):
    template_name = "chats/index.html"
    pk_url_kwarg = 'document_id'

    def get(self, request, *args, **kwargs):
        context = {}
        document_id = self.kwargs.get("document_id")
        session_id = generate_id()
        context["document_id"] = document_id
        context["session_id"] = session_id
        context["ws_url_params"] = f"{document_id}/?session_id={session_id}"

        return render(request, self.template_name, context)