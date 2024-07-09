# TODO
# TODO: Detect organization name from blog
# TODO: Classify blog post into categories
# TODO: Test on some blogs for evaluation


import os
import spacy
from spacy import displacy

# from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq

os.environ["GROQ_API_KEY"] = "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"
nlp = spacy.load("en_core_web_lg")  # using large spacy model for better accuracy
# llama_model = Ollama(model="llama3:8b")
llama_model = ChatGroq(model="llama3-8b-8192")


def detect_organization(blog_content):
    try:
        # Roberta base model
        doc = nlp(blog_content)
        options = {"ents": ["OGR"]}  # Only detecting organization
        organizations = [ent.text for ent in doc.ents if ent.label_ == "ORG"]
        organizations = list(set(organizations))  # removing duplicates
        return organizations
    except:
        return []


def classify_blog(blog_content):
    # using llama3:8b model running locally
    # Categories are :
    # 1. company_merger/acquisition/collaboration
    # 2. product_launch
    # 3. innovation/breaktrough/research in cosmatic
    try:
        prompt_template = """
        You are given a blog post and need to classify it into one or more of the following categories:
        1. Innovation in cosmetic/breakthrough in research
        2. Company merger/collaboration
        3. Product launch

        Carefully analyze the blog content to determine which of these categories it belongs to. If the blog fits into multiple categories, list all the relevant categories with comma seperated. If the blog does not fit any of these categories, respond with "None of category".

        Consider the following points while classifying:
        - If the blog discusses new scientific discoveries, technological advancements, or research breakthroughs in the cosmetic industry, classify it as "Innovation in cosmetic/breakthrough in research".
        - If the blog talks about companies merging, collaborating, or forming partnerships, classify it as "Company merger/collaboration".
        - If the blog describes the launch of a new product, including its features, benefits, or market introduction, classify it as "Product launch".

        Here is the blog content for classification:
        {blog_content}

        Please provide only the exact category names with comma seperated if there are multiple, or "None of category" if no categories apply, without any additional text.
        """
        prompt = ChatPromptTemplate.from_template(prompt_template)
        output_parser = StrOutputParser()
        chain = prompt | llama_model | output_parser
        response = chain.invoke({"blog_content": blog_content})
        return response.split(",")
    except:
        return []
