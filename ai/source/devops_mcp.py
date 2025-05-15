from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
# Libreria que permite ejecutar comandos en la terminal
import subprocess
# Libreria que permite enviar emails
import smtplib

# 1. Obtener logs del último despliegue fallido
def get_k8s_logs(pod_name):
  return subprocess.check_output(["kubectl", "logs", pod_name]).decode("utf-8")

# 2. Obtener commits recientes
def get_git_commits():
  return subprocess.check_output(["git", "log", "-3", "--pretty=format:%h - %s"]).decode("utf-8")

# 3. Generar post-mortem con LLM
def generate_postmortem(logs, commits):
  llm = ChatOpenAI()
  prompt = PromptTemplate.from_template(
    "Analiza los siguientes logs:\n{logs}\n\nY los siguientes commits:\n{commits}\n\nGenera un post-mortem técnico breve para un equipo DevOps."
  )
  chain = LLMChain(llm=llm, prompt=prompt)
  return chain.run({"logs": logs, "commits": commits})

# 4. Enviar el reporte
def send_email(report):
  # Ejemplo simple, puedes cambiarlo por Slack o Notion API
  with smtplib.SMTP('smtp.tu-servidor.com') as server:
    server.sendmail("agente@devopsbot.com", "equipo@midominio.com", report)

# Main
if __name__ == "__main__":
  logs = get_k8s_logs("backend-deployment-xyz")
  commits = get_git_commits()
  report = generate_postmortem(logs, commits)
  send_email(report)
