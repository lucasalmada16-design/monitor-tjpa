import requests
from bs4 import BeautifulSoup
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import PyPDF2
import io

EMAIL_USER = os.environ.get("EMAIL_USER")
EMAIL_PASS = os.environ.get("EMAIL_PASS")

SEU_NOME = "Lucas Almada de Sousa Martins"

BASE_URL = "https://dje.tjpa.jus.br"
URL = "https://dje.tjpa.jus.br/ClientDJEletronico/"


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


def obter_pdfs():

    response = requests.get(URL)

    soup = BeautifulSoup(response.text, "html.parser")

    pdfs = []

    for link in soup.find_all("a"):

        href = link.get("href")

        if href and ".pdf" in href.lower():

            if href.startswith("http"):
                pdfs.append(href)
            else:
                pdfs.append(BASE_URL + href)

    return pdfs


def verificar():

    pdfs = obter_pdfs()

    encontrou = False

    for pdf_url in pdfs:

        response = requests.get(pdf_url)

        pdf_bytes = response.content

        reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))

        paginas = []

        for i, page in enumerate(reader.pages):

            texto = page.extract_text()

            if texto and SEU_NOME.lower() in texto.lower():

                paginas.append(i+1)

        if paginas:

            encontrou = True

            enviar_email(
                "SEU NOME FOI ENCONTRADO — DJE TJPA",
                f"Arquivo: {pdf_url}\nPágina(s): {paginas}",
                pdf_bytes,
                "diario_encontrado.pdf"
            )

    if not encontrou:

        enviar_email(
            "Verificação concluída",
            "Seu nome não foi encontrado nos diários da semana passada."
        )


verificar()
