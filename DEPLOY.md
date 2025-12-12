# Deploy do Gerador de Currículo (Flask + WeasyPrint)

## 1. Dependências

- Python 3.10+ (recomendado)
- Bibliotecas Python: `Flask`, `WeasyPrint`, `gunicorn` (já listadas em `requirements.txt`)
- Dependências de sistema para o WeasyPrint (Cairo, Pango etc.). Em ambiente local Windows use o instalador oficial do WeasyPrint.

Instalação local de dependências Python:

```bash
pip install -r requirements.txt
```

---

## 2. Executar localmente (desenvolvimento)

```bash
# dentro da pasta do projeto
python app.py
```

Acesse em: http://127.0.0.1:5000/

---

## 3. Deploy no Railway

1. Crie um repositório no GitHub com este projeto.
2. No painel do Railway, crie um novo projeto a partir do repositório.
3. Certifique-se de que o Railway está usando `Python` como ambiente.
4. O Railway normalmente detecta o `Procfile` automaticamente com o comando:

```bash
web: gunicorn app:app
```

5. Garanta que `pip install -r requirements.txt` é executado no build.
6. Como o WeasyPrint depende de bibliotecas do sistema, se o PDF não gerar em produção, você pode:
   - Usar uma imagem Docker que já tenha Cairo/Pango instalados; ou
   - Seguir a documentação do Railway para instalar pacotes de sistema necessários.

A URL pública do Railway já usa HTTPS.

---

## 4. Deploy no Render.com

1. Crie um repositório Git com o projeto.
2. No painel do Render, crie um novo serviço do tipo **Web Service** a partir do repositório.
3. Selecione **Python** como runtime.
4. Configure:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
5. Deploy e teste a rota `/` e a geração de PDF.
6. Caso o PDF falhe por falta de libs do sistema, configure uma imagem customizada ou consulte a documentação do Render para adicionar Cairo/Pango.

O Render também fornece HTTPS automático.

---

## 5. Deploy no PythonAnywhere (plano gratuito)

1. Envie os arquivos do projeto (via Git ou upload) para seu diretório no PythonAnywhere.
2. No painel **Web**, crie um novo app **Flask** (versão manual).
3. No arquivo WSGI gerado pelo PythonAnywhere, importe o `app` deste projeto, por exemplo:

```python
from pathlib import Path
import sys

# ajuste o caminho conforme o seu usuário/pasta
project_root = Path('/home/seu_usuario/meucurriculo')
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from app import app as application
```

4. No ambiente virtual do PythonAnywhere, instale as dependências:

```bash
pip install -r /home/seu_usuario/meucurriculo/requirements.txt
```

5. Recarregue o app no painel Web e teste a geração do PDF.

O PythonAnywhere oferece HTTPS via domínio `https://seu_usuario.pythonanywhere.com`.

---

## 6. Observações de segurança

- Os dados não são salvos em disco; o PDF é gerado em memória e enviado diretamente ao cliente.
- O backend limita o tamanho dos campos para reduzir risco de abuso.
- Use sempre HTTPS na plataforma de hospedagem escolhida.
