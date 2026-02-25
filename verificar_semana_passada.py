import requests
import os
import smtplib
import io
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import PyPDF2

EMAIL_USER = os.environ.get("EMAIL_USER")
EMAIL_PASS = os.environ.get("EMAIL_PASS")

SEU_NOME = "Lucas Almada de Sousa Martins"
PALAVRA_CARGO = "Oficial de Justiça"

ANO = 2026
EDICAO_ATUAL = 8251   # ALTERE SE NECESSÁRIO

BASE_URL = "https://dje.tjpa.jus.br/DJEletronico/rest/DJEletronicoService/publicacao/visualizarDiarioPDF"


def enviar_email(assunto, mensagem, pdf_bytes=None, nome_pdf="diario.pdf"):

    msg = MIMEMultipart()
    msg['Subject'] = assunto
    msg['From'] = EMAIL_USER
    msg['To'] = EMAIL_USER

    msg.attach(MIMEText(mensagem))

    if pdf_bytes:
        part = MIMEApplication(pdf_bytes, Name=nome_pdf)
        part['Content-Disposition'] = f'attachment; filename="{nome_pdf}"'
        msg.attach(part)

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)


def verificar():

    encontrou_algo = False

    for i in range(7):

        numero_edicao = EDICAO_ATUAL - i

        url = f"{BASE_URL}/{numero_edicao}-{ANO}"

        response = requests.get(url)

        if response.status_code != 200:
            continue

        pdf_bytes = response.content

        reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))

        paginas_encontradas = []

        for num, page in enumerate(reader.pages):

            texto = page.extract_text()

            if not texto:
                continue

            texto_lower = texto.lower()

            if SEU_NOME.lower() in texto_lower or PALAVRA_CARGO.lower() in texto_lower:

                paginas_encontradas.append(num + 1)

        if paginas_encontradas:

            encontrou_algo = True

            enviar_email(
                f"TJPA — Encontrado na edição {numero_edicao}-{ANO}",
                f"Edição: {numero_edicao}-{ANO}\nPágina(s): {paginas_encontradas}",
                pdf_bytes,
                f"DJE_{numero_edicao}-{ANO}.pdf"
            )

    if not encontrou_algo:

        enviar_email(
            "TJPA — Verificação concluída",
            "Nenhuma ocorrência encontrada nas últimas 7 edições."
        )


verificar()
