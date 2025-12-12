# Gerador de Currículo Profissional

Aplicação web em **Python + Flask** para gerar currículos profissionais em PDF (e outros formatos) a partir de um formulário simples, em português.

O foco é facilitar a criação de currículos bem estruturados, com análise básica de vaga, upload de foto e templates pensados para leitura humana e sistemas ATS.

---

## Principais recursos

- Formulário completo com seções para:
  - Dados pessoais
  - Resumo profissional
  - Experiências
  - Formação
  - Habilidades (técnicas, comportamentais, outras)
  - Certificações, Projetos, Idiomas, Cursos, Prêmios, Voluntariado, Publicações
- **Upload de foto** ou uso de **URL da foto**, exibida no canto superior esquerdo, ao lado do nome.
- Geração de **PDF corporativo** com layout limpo e profissional usando **WeasyPrint**.
- Backend faz uma **análise simples da vaga** (via URL) para priorizar palavras‑chave nas habilidades.
- Exportação também suporta **Word (.docx)** e **JSON** (para reutilizar dados), embora na interface padrão a exportação esteja configurada para **PDF corporativo automático**.
- Pronto para deploy em plataformas como **Render**, **Railway**, **PythonAnywhere** ou via **Docker**.

---

## Arquitetura

- Backend: [Flask](https://flask.palletsprojects.com/) em [app.py](app.py)
- Geração de PDF: [WeasyPrint](https://weasyprint.org/)
- Geração de DOCX: [python-docx](https://python-docx.readthedocs.io/)
- Extração de palavras‑chave da vaga: `requests` + `beautifulsoup4`
- Frontend:
  - Formulário principal em [templates/index.html](templates/index.html)
  - Templates de currículo (PDF) em:
	 - [templates/resume_template.html](templates/resume_template.html) (corporativo)
	 - [templates/resume_template_minimal.html](templates/resume_template_minimal.html)
	 - [templates/resume_template_ats.html](templates/resume_template_ats.html)
  - Estilos em [static/css/style.css](static/css/style.css)
- Docker: imagem baseada em `python:3.11-slim` com todas as libs de sistema necessárias ao WeasyPrint ([Dockerfile](Dockerfile)).

> Observação: existe também um script experimental para uso com PyScript/Pyodide em páginas estáticas ([script.py](script.py)), mas o fluxo principal deste projeto é o backend Flask.

---

## Requisitos

- **Python 3.10+** (recomendado 3.11)
- Pip / ambiente virtual (opcional mas recomendado)

Para geração de PDF **fora do Docker**, o WeasyPrint precisa de bibliotecas gráficas do sistema (Cairo, Pango, Harfbuzz, etc.).

- No **Windows**, siga a documentação oficial do WeasyPrint:  
  https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#installation
- Em **Linux**, o Dockerfile deste projeto mostra os pacotes necessários (seção `RUN apt-get ...`).

Se você usar **Docker**, essas dependências já estão configuradas na imagem.

---

## Como rodar localmente (sem Docker)

1. Clone o repositório:

	```bash
	git clone https://github.com/propythonlab/meucurriculo.git
	cd meucurriculo
	```

2. (Opcional, mas recomendado) Crie e ative um ambiente virtual:

	```bash
	python -m venv .venv
	# Windows
	.venv\Scripts\activate
	# Linux/macOS
	# source .venv/bin/activate
	```

3. Instale as dependências Python:

	```bash
	pip install -r requirements.txt
	```

4. (Se necessário) configure o WeasyPrint no seu sistema conforme a documentação oficial.

5. Inicie o servidor Flask em modo desenvolvimento:

	```bash
	python app.py
	```

6. Acesse no navegador:

	- http://127.0.0.1:5000/

Preencha o formulário, envie a foto (opcional) e clique em **Gerar arquivo**. O PDF será baixado automaticamente e o formulário será limpo para um novo preenchimento.

---

## Rodando com Docker

O repositório já inclui um [Dockerfile](Dockerfile) configurado com todas as dependências de sistema do WeasyPrint.

1. Construa a imagem:

	```bash
	docker build -t meucurriculo .
	```

2. Rode o container (expondo a porta padrão 8000):

	```bash
	docker run -p 8000:8000 meucurriculo
	```

3. Acesse em:

	- http://127.0.0.1:8000/

Em plataformas PaaS (Render, Railway etc.), a aplicação usa a variável de ambiente `PORT` para definir a porta de escuta dentro do container.

---

## Deploy

O arquivo [DEPLOY.md](DEPLOY.md) traz um passo a passo mais detalhado para deploy em:

- **Railway**
- **Render.com**
- **PythonAnywhere**

Em resumo, você pode:

- Usar **Docker** (recomendado, pois já inclui as libs do WeasyPrint), ou
- Usar o ambiente Python da própria plataforma e instalar as dependências de sistema seguindo a documentação do WeasyPrint.

---

## Estrutura básica do código

- [app.py](app.py): rota `/` (formulário) e `/gerar` (monta os dados, faz análise simples da vaga, escolhe o template e gera PDF/Word/JSON).
- [templates/index.html](templates/index.html): HTML do formulário com JavaScript para clonar blocos dinâmicos e enviar o formulário via `fetch`.
- [templates/resume_template*.html](templates): templates de currículo usados pelo WeasyPrint.
- [static/css/style.css](static/css/style.css): estilos da página do formulário.
- [Dockerfile](Dockerfile): imagem para produção contendo Python, libs do sistema e o app servido via `gunicorn`.

---

## Licença

Este projeto é de uso educacional/demonstração. Adapte a estrutura, textos e estilos conforme a sua necessidade antes de usar em produção.

