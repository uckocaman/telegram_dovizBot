import time
import json
import telebot
import requests

bot_token = "BotFather tarafından verilen token bilgisi"
bot = telebot.TeleBot(token=bot_token)

@bot.message_handler(commands=['bilgi'])
def bilgi(message):
    bot.send_message(message.chat.id, """
        Hosgeldiniz. Güncel döviz kurlarını öğrenmek için /kurBilgi yazabilirsiniz. Döviz çevirisi yapmak için /ceviri yazıktan sonra aralarında bir boşluk bırakarak önce miktarı, daha sonra elinizdeki para birimini son olarak da çevirmek istediğiniz para birimini aşağıdaki gibi girin.
        
        Türk Lirası -> TRY
        Dolar -> USD
        Euro -> EUR
        Sterlin -> GBP

Örneğin 100 Dolar'ın kaç Türk Lirası'na karşılık geldiğini öğrenmek isterseniz:
        /ceviri 100 USD TL""")

@bot.message_handler(commands=['kurBilgi'])
def kutBilgi(message):
    dolar_api_url = "https://api.exchangeratesapi.io/latest?base=USD"
    euro_api_url = "https://api.exchangeratesapi.io/latest?base=EUR"
    gbp_api_url = "https://api.exchangeratesapi.io/latest?base=GBP"

    dolar_result = json.loads(requests.get(dolar_api_url).text)
    eur_result = json.loads(requests.get(euro_api_url).text)
    gbp_result = json.loads(requests.get(gbp_api_url).text)

    bot.send_message(message.chat.id, f'USD: {round(dolar_result["rates"]["TRY"],4)} TL\nEUR: {round(eur_result["rates"]["TRY"],4)} TL\nGBP: {round(gbp_result["rates"]["TRY"],4)} TL')
    bot.send_message(message.chat.id, "İşlemler hakkında bilgi almak için /bilgi")

@bot.message_handler(commands=['ceviri'])
def ceviri(message):
    api_url = "https://api.exchangeratesapi.io/latest?base="
    get_name = message.text.split(' ')
    miktar = get_name[1]
    birim = get_name[2].upper()
    yeni_birim = get_name[3].upper()

    if yeni_birim == 'TL':
        yeni_birim = 'TRY'
    if birim == 'TL':
        birim = 'TRY'
    result = json.loads(requests.get(api_url+birim).text)
    sonuc = float(miktar) * result['rates'][str(yeni_birim)]
    bot.send_message(message.chat.id, f"{miktar} {birim} = {round(sonuc,5)} {yeni_birim}")
    
while True:
    try:
        bot.polling(none_stop=True)
    except Exception:
        time.sleep(15)
