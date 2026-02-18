import requests
import os
import smtplib
import io
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import PyPDF2

EMAIL_USER = os.environ.get("EMAIL_USER")
EMAIL_PASS = os.environ.get("EMAIL_PASS")

SEU_NOME = "Lucas Almada de Sousa Martins"

# URL base correta do DJE
BASE = "https://dje.tjpa.jus.br"

# Endpoint real dos PDFs
PDF_URL = BASE + "/ClientDJEletronico/PDF.aspx"


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


def baixar_pdf_por_data(data):

    data_str = data.strftime("%d/%m/%Y")

    params = {
        "data": data_str
    }

    response = requests.get(PDF_URL, params=params)

    if response.status_code == 200 and len(response.content) > 5000:

        return response.content

    return None


def verificar():

    hoje = datetime.today()

    encontrou = False

    for i in range(7):

        data = hoje - timedelta(days=i)

        pdf_bytes = baixar_pdf_por_data(data)

        if not pdf_bytes:
            continue

        reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))

        paginas = []

        for num, page in enumerate(reader.pages):

            texto = page.extract_text()

            if texto and SEU_NOME.lower() in texto.lower():

                paginas.append(num+1)

        if paginas:

            encontrou = True

            enviar_email(
                "SEU NOME FOI ENCONTRADO NO DJE",
                f"Data: {data.strftime('%d/%m/%Y')}\nPágina(s): {paginas}",
                pdf_bytes,
                f"DJE_{data.strftime('%Y%m%d')}.pdf"
            )

    if not encontrou:

        enviar_email(
            "Verificação DJE concluída",
            "Seu nome não foi encontrado na última semana."
        )


verificar()
