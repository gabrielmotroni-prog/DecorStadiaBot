# -*- coding: utf-8 -*-
#arquivo princpal da regra de negocio das nossas aplicacao
#ira controlar toda nossas nossa aplicacao por meio das rotas de protocolo http
from operator import eq
from re import A
from flask import render_template, request, url_for, redirect, flash, jsonify,session, abort, redirect
from requests.models import HTTPBasicAuth
from werkzeug.wrappers import AuthorizationMixin
from app import  app, db
from telebot import types
import os

#Biblioteca para o bot do telegram
import telebot
import urllib
#-------------variavel de ambiente
from dotenv import load_dotenv
load_dotenv()  # obtém variáveis ​​de ambiente de .env.
MY_ENV_VAR = os.getenv('MY_ENV_VAR')
env_chave_api_bot = os.getenv('env_chave_api_bot')
print(MY_ENV_VAR)
#--------------- 

#configurações do bot
chave_api = env_chave_api_bot
bot = telebot.TeleBot(chave_api)



@app.route("/")
def index():
    
  
    return render_template("index.html")

#Opção de fotos das decorações
def finalidades(mensagem):
    imagens = {'HomeOffice': ['https://raw.githubusercontent.com/gabrielmotroni-prog/DecorStadiaBot/main/app/images/homeoffice1.jpg', 'https://raw.githubusercontent.com/gabrielmotroni-prog/DecorStadiaBot/main/app/images/homeoffice2.png'],
                'Sala': ['https://raw.githubusercontent.com/gabrielmotroni-prog/DecorStadiaBot/main/app/images/sala1.jpg', 'https://raw.githubusercontent.com/gabrielmotroni-prog/DecorStadiaBot/main/app/images/sala2.jpg'],
                'Suite': ['https://raw.githubusercontent.com/gabrielmotroni-prog/DecorStadiaBot/main/app/images/suite1.jpg', 'https://raw.githubusercontent.com/gabrielmotroni-prog/DecorStadiaBot/main/app/images/suite2.jpg'],
                'Quarto': ['https://raw.githubusercontent.com/gabrielmotroni-prog/DecorStadiaBot/main/app/images/quarto1.jpg', 'https://raw.githubusercontent.com/gabrielmotroni-prog/DecorStadiaBot/main/app/images/quarto2.jpg']
                }
    if mensagem.text == '/HomeOffice':
        #bot.send_photo(mensagem.chat.id, imagens['HomeOffice'][0])
        bot.send_photo(mensagem.chat.id, imagens['HomeOffice'][0])
        bot.send_photo(mensagem.chat.id, imagens['HomeOffice'][1])

    elif mensagem.text == '/Sala':
        bot.send_photo(mensagem.chat.id, imagens['Sala'][0])
        bot.send_photo(mensagem.chat.id, imagens['Sala'][1])
    elif mensagem.text == '/Suite':
        bot.send_photo(mensagem.chat.id, imagens['Suite'][0])
        bot.send_photo(mensagem.chat.id, imagens['Suite'][1])
    elif mensagem.text == '/Quarto':
        bot.send_photo(mensagem.chat.id, imagens['Quarto'][0])
        bot.send_photo(mensagem.chat.id, imagens['Quarto'][1])


@bot.message_handler(func=finalidades)
def responder_finalidades(mensagem):
    return True

@bot.message_handler(commands=["Voltar"])
def menu_principal(mensagem):
    msg = '''/Decoracoes - Ver decorações realizadas dos nossos clientes
/Designer - Falar com nossos designers de interiores
/Loja - Ir para a loja'''
    fileira = types.ReplyKeyboardMarkup(row_width=2)
    b1 = types.KeyboardButton('/Decoracoes')
    b2 = types.KeyboardButton('/Designer')
    b3 = types.KeyboardButton('/Loja')
    fileira.add(b1, b2, b3)
    bot.reply_to(mensagem, msg, reply_markup=fileira)

@bot.message_handler(commands=['Decoracoes'])
def decoracoes(mensagem):
    msg = '''Por favor, escolha qual finalidade:
    '''
    fileira = types.ReplyKeyboardMarkup(row_width=2)
    b1 = types.KeyboardButton('/HomeOffice')
    b2 = types.KeyboardButton('/Sala')
    b3 = types.KeyboardButton('/Suite')
    b4 = types.KeyboardButton('/Quarto')
    b5 = types.KeyboardButton('/Voltar')
    fileira.add(b1, b2, b3, b4, b5)
    bot.send_message(mensagem.chat.id, msg, reply_markup=fileira)
    
@bot.message_handler(commands=["Loja"])
def loja(mensagem):
    msg = '''Em desenvolvimento
/Voltar'''
    bot.reply_to(mensagem, msg)

@bot.message_handler(commands=["Designer"])
def designers(mensagem):
    msg = '''Gabriel: https://api.whatsapp.com/send?phone=5511846548844

    Priscila: https://api.whatsapp.com/send?phone=5511246548741

    Bruno: https://api.whatsapp.com/send?phone=5512246548223

    /Voltar'''

    bot.reply_to(mensagem, msg)

@bot.message_handler(commands=["start"])
def apresentacao(mensagem):
    msg = '''Olá, sou o Assistente Virtual do Decor Stadia, prazer! 😁
    Por favor, clicar na opção desejada:

    /Decoracoes - Ver decorações realizadas para os nossos clientes
    /Designer - Falar com nossos designers de interiores
    /Loja - Ir para a loja
    '''
    fileira = types.ReplyKeyboardMarkup(row_width=2)
    b1 = types.KeyboardButton('/Decoracoes')
    b2 = types.KeyboardButton('/Designer')
    b3 = types.KeyboardButton('/Loja')
    fileira.add(b1, b2, b3)
    bot.reply_to(mensagem, msg, reply_markup=fileira)

def qualquer_mensagem(mensagem):
    return True

@bot.message_handler()
def responder(mensagem):
    comandos = ['/Decoracoes', '/Designer', '/Loja', '/HomeOffice', '/Sala', '/Suite', '/Quarto', '/Voltar']
    if mensagem.text not in comandos:
        bot.send_message(mensagem.chat.id, "Desculpe, não reconheço este comando")

bot.polling()