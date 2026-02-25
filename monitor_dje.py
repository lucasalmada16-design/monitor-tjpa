import requests
import io
import os
import smtplib
from email.message import EmailMessage
import PyPDF2

EMAIL = os.environ.get("EMAIL_USER")
SENHA_APP = os.environ.get("EMAIL_PASS")

SEU_NOME = "Lucas Almada de Sousa Martins"

ANO = 2026

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


def descobrir_edicao_recente():

    # começa procurando de um número alto
    for numero in range(9000, 8000, -1):

        url = f"{BASE_URL}/{numero}-{ANO}"

        r = requests.get(url)

        if r.status_code == 200 and len(r.content) > 10000:
            return numero, url, r.content

    return None, None, None


def verificar_edicao_mais_recente():

    numero, url, pdf_bytes = descobrir_edicao_recente()

    if not numero:
        print("Não foi possível descobrir a edição mais recente.")
        return

    print("Edição mais recente encontrada:", numero)

    reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))

    paginas_encontradas = []

    for pagina_num, pagina in enumerate(reader.pages):

        texto = pagina.extract_text()

        if not texto:
            continue

        if SEU_NOME.lower() in texto.lower():
            paginas_encontradas.append(pagina_num + 1)

    if paginas_encontradas:

        corpo_email = (
            f"🚨 SEU NOME FOI ENCONTRADO\n\n"
            f"Edição: {numero}-{ANO}\n"
            f"Páginas: {paginas_encontradas}\n\n"
            f"Link direto:\n{url}"
        )

        enviar_email(
            "🚨 TJPA — SEU NOME FOI ENCONTRADO",
            corpo_email
        )

        print("Nome encontrado e email enviado.")

    else:
        print("Nome não encontrado na edição mais recente.")


verificar_edicao_mais_recente()
