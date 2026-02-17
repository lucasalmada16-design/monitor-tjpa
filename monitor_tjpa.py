import requests
from bs4 import BeautifulSoup
import os
import smtplib
from email.mime.text import MIMEText

EMAIL_USER = os.environ.get("EMAIL_USER")
EMAIL_PASS = os.environ.get("EMAIL_PASS")

SEU_NOME = "Lucas Almada de Sousa Martins"

# Lista de páginas do diário (últimos dias)
URLS = [
    "https://www.tjpa.jus.br/PortalExterno/diario/",
    "https://www.tjpa.jus.br/PortalExterno/diario/?page=1",
    "https://www.tjpa.jus.br/PortalExterno/diario/?page=2",
    "https://www.tjpa.jus.br/PortalExterno/diario/?page=3",
    "https://www.tjpa.jus.br/PortalExterno/diario/?page=4",
    "https://www.tjpa.jus.br/PortalExterno/diario/?page=5"
]

def enviar_email(assunto, mensagem):
    msg = MIMEText(mensagem)
    msg['Subject'] = assunto
    msg['From'] = EMAIL_USER
    msg['To'] = EMAIL_USER

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)

def verificar():
    encontrou = False

    for url in URLS:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        texto = soup.get_text().lower()

        if SEU_NOME.lower() in texto:
            enviar_email(
                "SEU NOME FOI ENCONTRADO NO DJE TJPA",
                f"Seu nome foi encontrado nesta página:\n{url}"
            )
            encontrou = True

    if not encontrou:
        enviar_email(
            "Verificação concluída",
            "Seu nome não foi encontrado nos últimos diários verificados."
        )

verificar()
