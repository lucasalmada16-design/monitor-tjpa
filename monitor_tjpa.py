import requests
from bs4 import BeautifulSoup
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import PyPDF2
import io

EMAIL_USER = os.environ.get("EMAIL_USER")
EMAIL_PASS = os.environ.get("EMAIL_PASS")

SEU_NOME = "Lucas Almada de Sousa Martins"

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

def obter_link_pdf():

    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")

    links = soup.find_all("a")

    for link in links:

        href = link.get("href")

        if href and ".pdf" in href.lower():

            if href.startswith("http"):
                return href
            else:
                return URL + href

    return None

def verificar_pdf():

    link_pdf = obter_link_pdf()

    if not link_pdf:

        enviar_email(
            "Erro monitor TJPA",
            "Não foi possível encontrar o PDF do diário."
        )

        return

    response = requests.get(link_pdf)

    pdf_bytes = response.content

    reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))

    encontrou = False

    paginas_encontradas = []

    for i, page in enumerate(reader.pages):

        texto = page.extract_text()

        if texto:

            texto_lower = texto.lower()

            if SEU_NOME.lower() in texto_lower or "oficial de justiça" in texto_lower:

                encontrou = True

                paginas_encontradas.append(i + 1)

    if encontrou:

        enviar_email(
            "TJPA — Nomeação encontrada",
            f"Encontrado na(s) página(s): {paginas_encontradas}\nPDF em anexo.",
            pdf_bytes
        )

    else:

        enviar_email(
            "TJPA — Verificação concluída",
            "Nenhuma nomeação encontrada no diário mais recente."
        )

verificar_pdf()
