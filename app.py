import time
import json
import telebot
import requests
import locale

bot_token = "BotFather tarafından verilen token bilgisi"
bot = telebot.TeleBot(token=bot_token)

@bot.message_handler(commands=['bilgi'])
def bilgi(message):
    bot.send_message(message.chat.id, """
        Hosgeldiniz. Güncel döviz kurlarını öğrenmek için /kurBilgi, kripto para fiyatları için /coinBilgi yazabilirsiniz. Döviz çevirisi yapmak için /ceviri yazıktan sonra aralarında bir boşluk bırakarak önce miktarı, daha sonra elinizdeki para birimini son olarak da çevirmek istediğiniz para birimini aşağıdaki gibi girin.
        
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
    kurMesaj = f'''
USD :       {round(dolar_result["rates"]["TRY"],4)}
EUR :       {round(eur_result["rates"]["TRY"],4)}
GBP :       {round(gbp_result["rates"]["TRY"],4)}
    '''
    bot.send_message(message.chat.id, kurMesaj, parse_mode="Markdown")

@bot.message_handler(commands=['coinBilgi'])
def coinBilgi(message):
    locale.setlocale(locale.LC_ALL, '')

    dolar_api_url = "https://api.exchangeratesapi.io/latest?base=USD"
    dolar_result = json.loads(requests.get(dolar_api_url).text)
    tl = dolar_result['rates']['TRY']
    api_token = "nomics.com'dan alınan API Token"
    url = f"https://api.nomics.com/v1/currencies/ticker?key={api_token}&ids=BTC,ETH,LTC,DOT"

    response = requests.get(url)
    data = response.json()
    btc = data[0]['price']
    eth = data[1]['price']
    ltc = data[2]['price']
    dot = data[3]['price']

    coinMesaj = F"""<pre>
| Coins |    USD    |     TL    |
|-------|:---------:|----------:|
| BTC   | {locale.format_string('%.2f', float(btc), grouping=True)} | {locale.format_string('%.2f', float(btc) * float(tl), grouping=True)}|
| ETH   | {locale.format_string('%.2f', float(eth), grouping=True)}  | {locale.format_string('%.2f', float(eth) * float(tl), grouping=True)}  |
| LTC   | {locale.format_string('%.2f', float(ltc), grouping=True)}     | {locale.format_string('%.2f', float(ltc) * float(tl), grouping=True)}    |
| DOT   | {locale.format_string('%.2f', float(dot), grouping=True)}    | {locale.format_string('%.2f', float(dot) * float(tl), grouping=True)}    |
</pre>"""
    bot.send_message(message.chat.id, coinMesaj, parse_mode="HTML")

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
