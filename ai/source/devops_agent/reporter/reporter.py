# reporter/reporter.py
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

def generate_report(summary):
  prompt = PromptTemplate.from_template(
    "Eres un ingeniero DevOps. Genera un informe post-mortem con este resumen:\n{summary}\nFormato profesional."
  )
  chain = LLMChain(llm=ChatOpenAI(), prompt=prompt)
  return chain.run({"summary": summary})
