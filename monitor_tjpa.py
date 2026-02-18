import requests
from bs4 import BeautifulSoup
import os
import smtplib
from email.mime.text import MIMEText
import PyPDF2
import io

EMAIL_USER = os.environ.get("EMAIL_USER")
EMAIL_PASS = os.environ.get("EMAIL_PASS")

SEU_NOME = "Lucas Almada de Sousa Martins"

BASE_URL = "https://www.tjpa.jus.br"

def enviar_email(assunto, mensagem):
    msg = MIMEText(mensagem)
    msg['Subject'] = assunto
    msg['From'] = EMAIL_USER
    msg['To'] = EMAIL_USER

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)

def ler_pdf(url_pdf):

    response = requests.get(url_pdf)

    pdf_file = io.BytesIO(response.content)

    reader = PyPDF2.PdfReader(pdf_file)

    texto = ""

    for page in reader.pages:
        texto += page.extract_text()

    return texto.lower()

def verificar_diarios():

    response = requests.get("https://www.tjpa.jus.br/PortalExterno/diario/")
    soup = BeautifulSoup(response.text, "html.parser")

    links = soup.find_all("a")

    encontrou = False

    for link in links:

        href = link.get("href")

        if href and ".pdf" in href.lower():

            url_pdf = BASE_URL + href

            texto_pdf = ler_pdf(url_pdf)

            if SEU_NOME.lower() in texto_pdf:

                enviar_email(
                    "URGENTE — SEU NOME FOI ENCONTRADO NO DJE TJPA",
                    f"Seu nome foi encontrado neste diário:\n{url_pdf}"
                )

                encontrou = True

    if not encontrou:

        enviar_email(
            "Verificação concluída",
            "Seu nome não foi encontrado nos diários verificados."
        )

verificar_diarios()
