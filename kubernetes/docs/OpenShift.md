# OpenShift

## Adminstracion
- `oc must-gather` (cmd: `oc must-gather --dest-dir <dir>`)
Recopila una fotografía exhaustiva (logs, configs, eventos) de todo el clúster en un .tar.gz para diagnósticos profundos o soporte técnico. Es tu "todo en uno" cuando algo falla globalmente.

- `oc adm inspect` (cmd: `oc adm inspect <recurso> --dest-dir <dir> [--since <tiempo>]`)
Proporciona un diagnóstico detallado y enfocado de un recurso específico (ej., un operador o Pod) en un directorio local. Es para investigar problemas puntuales de un componente en un momento dado, ideal para depuración dirigida.
