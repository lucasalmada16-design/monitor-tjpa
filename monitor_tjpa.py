
import os
import json
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
from openpyxl import load_workbook

CONFIG_FILE = "config.json"
HISTORICO_FILE = "historico_nomeacoes.xlsx"

def carregar_config():
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def enviar_email(config, assunto, mensagem):
    msg = MIMEText(mensagem)
    msg['Subject'] = assunto
    msg['From'] = config["email_remetente"]
    msg['To'] = config["email_destino"]

    with smtplib.SMTP(config["smtp_servidor"], config["smtp_porta"]) as server:
        server.starttls()
        server.login(config["email_remetente"], config["email_senha"])
        server.send_message(msg)

def salvar_historico(data, nome, cargo, edicao, seu_nome):
    wb = load_workbook(HISTORICO_FILE)
    ws = wb.active
    ws.append([data, nome, cargo, edicao, seu_nome])
    wb.save(HISTORICO_FILE)

def verificar_diario():
    # ESTE TRECHO É UM MODELO
    # Aqui você poderá integrar com download automático do DJE do TJPA
    
    config = carregar_config()
    
    # Exemplo fictício de teste
    data = datetime.now().strftime("%d/%m/%Y")
    nome = "EXEMPLO DE TESTE"
    cargo = "Oficial de Justiça"
    edicao = "0000"
    
    seu_nome = "SIM" if nome.lower() == config["nome_usuario"].lower() else "NÃO"
    
    salvar_historico(data, nome, cargo, edicao, seu_nome)
    
    assunto = "Monitor TJPA - Nova verificação realizada"
    mensagem = f"Verificação concluída em {data}\nNome encontrado: {nome}\nCargo: {cargo}"
    
    enviar_email(config, assunto, mensagem)

if __name__ == "__main__":
    verificar_diario()
