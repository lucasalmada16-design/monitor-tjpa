import requests
from bs4 import BeautifulSoup
import os
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

EMAIL_USER = os.environ.get("EMAIL_USER")
EMAIL_PASS = os.environ.get("EMAIL_PASS")

SEU_NOME = "Lucas Almada de Sousa Martins"

URL = "https://www.tjpa.jus.br/PortalExterno/diario/"

def enviar_email(assunto, mensagem):
    msg = MIMEText(mensagem)
    msg['Subject'] = assunto
    msg['From'] = EMAIL_USER
    msg['To'] = EMAIL_USER

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)

def verificar_diario():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")

    texto = soup.get_text().lower()

    if "oficial de justiça" in texto:
        enviar_email(
            "TJPA — Nova nomeação encontrada",
            "Uma nova nomeação de Oficial de Justiça foi publicada."
        )

    if SEU_NOME.lower() in texto:
        enviar_email(
            "URGENTE — SEU NOME FOI ENCONTRADO NO TJPA",
            "Seu nome apareceu no Diário Oficial do TJPA."
        )

verificar_diario()
