import requests
import io
import os
import smtplib
from email.message import EmailMessage
import PyPDF2

# =============================
# CONFIGURAÇÃO
# =============================

EMAIL = os.environ.get("EMAIL_USER")
SENHA_APP = os.environ.get("EMAIL_PASS")

SEU_NOME = "Lucas Almada de Sousa Martins"

ANO = 2026
EDICAO_INICIAL = 8244
EDICAO_FINAL = 8259

# =============================

BASE_URL = "https://dje.tjpa.jus.br/DJEletronico/rest/DJEletronicoService/publicacao/visualizarDiarioPDF"


def enviar_email(assunto, corpo):

    msg = EmailMessage()
    msg["Subject"] = assunto
    msg["From"] = EMAIL
    msg["To"] = EMAIL
    msg.set_content(corpo)

    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.starttls()
        smtp.login(EMAIL, SENHA_APP)
        smtp.send_message(msg)


def verificar_mes():

    encontrados = []

    for numero in range(EDICAO_INICIAL, EDICAO_FINAL + 1):

        url = f"{BASE_URL}/{numero}-{ANO}"

        print("Verificando edição:", numero)

        r = requests.get(url)

        if r.status_code != 200:
            continue

        pdf_bytes = r.content

        reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))

        for pagina_num, pagina in enumerate(reader.pages):

            texto = pagina.extract_text()

            if not texto:
                continue

            if SEU_NOME.lower() in texto.lower():

                encontrados.append(
                    f"Edição {numero}-{ANO} | Página {pagina_num+1}\nLink: {url}\n"
                )

    if encontrados:

        corpo_email = "🚨 SEU NOME FOI ENCONTRADO NO DJE:\n\n"

        for item in encontrados:
            corpo_email += item + "\n"

        enviar_email(
            "🚨 TJPA — SEU NOME FOI ENCONTRADO",
            corpo_email
        )

        print("Nome encontrado e email enviado.")

    else:
        print("Nenhuma ocorrência encontrada.")


verificar_mes()
