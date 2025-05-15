# trigger/detect_failure.py
import requests

def check_ci_failure():
  # Aquí conectas a GitHub API o similar
  return True  # Simulación

if __name__ == "__main__":
  if check_ci_failure():
    print("Fallo detectado")
