from js import document, window  # type: ignore
from pyodide.ffi import create_proxy  # type: ignore
import json


def _get_value(scope, selector: str) -> str:
    el = scope.querySelector(selector)
    return el.value.strip() if el and getattr(el, "value", None) is not None else ""


def collect_form_data(event=None):
    form = document.getElementById("cv-form")

    def gv(name: str) -> str:
        return _get_value(form, f"[name='{name}']")

    data = {
        "nome": gv("nome"),
        "titulo": gv("titulo"),
        "email": gv("email"),
        "telefone": gv("telefone"),
        "endereco": gv("endereco"),
        "portfolio": gv("link_portfolio"),
        "foto_url": gv("foto_url"),
        "resumo": gv("resumo"),
        # job_url é apenas informativo neste modo estático
    }

    # Experiências
    experiencias = []
    for item in document.querySelectorAll("#experiencias-container .experiencia-item"):
        exp = {
            "empresa": _get_value(item, "[name='exp_empresa']"),
            "cargo": _get_value(item, "[name='exp_cargo']"),
            "periodo": _get_value(item, "[name='exp_periodo']"),
            "local": _get_value(item, "[name='exp_local']"),
            "descricao": _get_value(item, "[name='exp_descricao']"),
            "conquistas": _get_value(item, "[name='exp_conquistas']"),
            "tecnologias": _get_value(item, "[name='exp_tech']"),
        }
        if any(exp.values()):
            experiencias.append(exp)
    data["experiencias"] = experiencias

    # Formações
    formacoes = []
    for item in document.querySelectorAll("#formacoes-container .experiencia-item"):
        edu = {
            "curso": _get_value(item, "[name='edu_curso']"),
            "instituicao": _get_value(item, "[name='edu_inst']"),
            "cidade": _get_value(item, "[name='edu_cidade']"),
            "ano": _get_value(item, "[name='edu_ano']"),
            "status": _get_value(item, "[name='edu_status']"),
        }
        if any(edu.values()):
            formacoes.append(edu)
    data["formacoes"] = formacoes

    # Habilidades
    def parse_skills(raw: str):
        return [s.strip() for s in raw.split(",") if s.strip()]

    data["skills_tecnicas"] = parse_skills(gv("skills_tecnicas"))
    data["skills_comportamentais"] = parse_skills(gv("skills_comportamentais"))
    data["skills_outras"] = parse_skills(gv("skills_outras"))

    # Certificações
    certificacoes = []
    for item in document.querySelectorAll("#certificacoes-container .experiencia-item"):
        cert = {
            "nome": _get_value(item, "[name='cert_nome']"),
            "instituicao": _get_value(item, "[name='cert_inst']"),
            "ano": _get_value(item, "[name='cert_ano']"),
            "codigo": _get_value(item, "[name='cert_codigo']"),
        }
        if any(cert.values()):
            certificacoes.append(cert)
    data["certificacoes"] = certificacoes

    # Projetos
    projetos = []
    for item in document.querySelectorAll("#projetos-container .experiencia-item"):
        proj = {
            "nome": _get_value(item, "[name='proj_nome']"),
            "tecnologias": _get_value(item, "[name='proj_tec']"),
            "descricao": _get_value(item, "[name='proj_desc']"),
            "link": _get_value(item, "[name='proj_link']"),
        }
        if any(proj.values()):
            projetos.append(proj)
    data["projetos"] = projetos

    # Idiomas
    idiomas = []
    for item in document.querySelectorAll("#idiomas-container .experiencia-item"):
        idi = {
            "nome": _get_value(item, "[name='idioma_nome']"),
            "nivel": _get_value(item, "[name='idioma_nivel']"),
        }
        if any(idi.values()):
            idiomas.append(idi)
    data["idiomas"] = idiomas

    # Cursos extra
    cursos_extra = []
    for item in document.querySelectorAll("#cursos-extra-container .experiencia-item"):
        ce = {
            "nome": _get_value(item, "[name='curso_extra_nome']"),
            "carga": _get_value(item, "[name='curso_extra_carga']"),
            "instituicao": _get_value(item, "[name='curso_extra_inst']"),
            "ano": _get_value(item, "[name='curso_extra_ano']"),
        }
        if any(ce.values()):
            cursos_extra.append(ce)
    data["cursos_extra"] = cursos_extra

    # Prêmios
    premios = []
    for item in document.querySelectorAll("#premios-container .experiencia-item"):
        pr = {
            "titulo": _get_value(item, "[name='premio_titulo']"),
            "instituicao": _get_value(item, "[name='premio_inst']"),
            "ano": _get_value(item, "[name='premio_ano']"),
            "descricao": _get_value(item, "[name='premio_desc']"),
        }
        if any(pr.values()):
            premios.append(pr)
    data["premios"] = premios

    # Voluntariado
    voluntariados = []
    for item in document.querySelectorAll("#voluntariado-container .experiencia-item"):
        vol = {
            "organizacao": _get_value(item, "[name='vol_org']"),
            "funcao": _get_value(item, "[name='vol_funcao']"),
            "periodo": _get_value(item, "[name='vol_periodo']"),
            "descricao": _get_value(item, "[name='vol_desc']"),
        }
        if any(vol.values()):
            voluntariados.append(vol)
    data["voluntariados"] = voluntariados

    data["publicacoes_texto"] = gv("publicacoes")

    output_format = gv("output_format") or "pdf"

    if output_format == "json":
        json_str = json.dumps(data, ensure_ascii=False, indent=2)
        blob = window.Blob.new([json_str], {"type": "application/json;charset=utf-8"})
        url = window.URL.createObjectURL(blob)
        a = document.createElement("a")
        a.href = url
        safe_name = (data.get("nome") or "curriculo").lower().replace(" ", "_")
        a.download = f"curriculo_{safe_name}.json"
        document.body.appendChild(a)
        a.click()
        document.body.removeChild(a)
        window.URL.revokeObjectURL(url)
    else:
        # Geração de PDF via jsPDF (função JS definida em index.html)
        data_json = json.dumps(data, ensure_ascii=False)
        window.gerarPDFFromJson(data_json)


# Conectar o botão ao handler Python
button = document.getElementById("btn-gerar")
if button is not None:
    button.onclick = create_proxy(collect_form_data)
