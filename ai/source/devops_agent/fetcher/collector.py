# fetcher/collector.py
# Libreria que permite ejecutar comandos en la terminal
import subprocess

def get_logs(pod_name="backend-xyz"):
  return subprocess.check_output(["kubectl", "logs", pod_name]).decode()

def get_commits(n=3):
  return subprocess.check_output(["git", "log", f"-{n}", "--pretty=format:%h - %s"]).decode()
