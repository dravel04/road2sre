# analyzer/analyzer.py
from memory.memory import load_history

def analyze(logs, commits):
  # Placeholder: añadir LLM o reglas
  past = load_history()
  return f"Resumen: posible error en despliegue. Últimos commits:\n{commits}\nHistorial: {len(past)} errores anteriores"
