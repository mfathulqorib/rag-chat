from mistralai import Mistral
import os


MISTRAL_API_KEY = os.environ["MISTRAL_API_KEY"]

mistral = Mistral(api_key=MISTRAL_API_KEY)
