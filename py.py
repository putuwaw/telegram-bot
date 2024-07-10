import telebot
import requests
import urllib
import time
import random
from datetime import datetime
import hashlib, random
import sqlite3
import json
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import os
from telebot import types

# Telegram API anahtarları buraya girin
api_token = '6979485535:AAFZdAsGmDJeCfBJbgY9PcOH2vus0enr54I'

bot = telebot.TeleBot(api_token)

sudo_users = [" "]
bot_owner_chat_id =[" "]
banned_users_file = "yasaklilar.txt"

@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    button1 = telebot.types.InlineKeyboardButton("🥷𝚂𝙰𝙷𝙸𝙿 🥷", url="https://t.me/HackedTCK")
    button2 = telebot.types.InlineKeyboardButton("👻ᴋᴀɴᴀʟ👻", url="https://t.me/lostblod")
    button3 = telebot.types.InlineKeyboardButton("🍓𝐂𝐇𝐀𝐓🍓", url="https://t.me/loostbloodarsiv")
    markup.add(button1, button2, button3)
    bot.reply_to(message, "👋 @ErthoBot 𝚂𝚘𝚛𝚞𝚐𝚞 𝚋𝚘𝚝𝚞𝚗𝚊 𝚑𝚘𝚜̧𝚐𝚎𝚕𝚍𝚒𝚗 /sorgular 𝚢𝚊𝚣𝚊𝚛𝚊𝚔 𝚔𝚘𝚖𝚞𝚝𝚕𝚊𝚛ｪ 𝚘̈𝚐𝚛𝚎𝚗𝚎𝚋𝚒𝚕𝚒𝚛𝚜𝚒𝚗 𝚒𝚢𝚒 𝚜𝚘𝚛𝚐𝚞𝚕𝚊𝚛.", reply_markup=markup)

@bot.message_handler(commands=['sorgular'])
def send_help_message(message):
    bot.reply_to(message, """
🤤 /tc komutu kullanarak Kişi Bilgi Alabilirsin
🤗 /adsoyad  komutu ile -isim -Soyisim -İl -İlce Sorgulama Yapar.
🥳 /aile komutu kullanarak aile sorgulama yapar.
🤩 /iban komutu ile banka bilgisi Alabilirsin.
😇 /tcgsm tcden gsm sorgu ceker.
🥶 /operator operatör sorgusu.
🥰 /kizlik kizlik soyadı sorgusu.
💌 /adres adres sorgusu.
💋 /burc burç sorgusu.
😶‍🌫 /sicil sicil kayıt sorgusu.
🥷/gsmtc gsm den tc sorgu çeker.
🤠 /yaz istediğiniz metini deftere yazar.
👩‍💻/sms sms bomber sorgusu yapar.
    """)
    
@bot.message_handler(commands=['sms'])
def send_sms(message):
    chat_id = message.chat.id
    user_input = message.text.split(' ', 1)

    if len(user_input) != 2:
        bot.send_message(chat_id, "Lütfen geçerli bir telefon numarası girin. örnek:\n\n/sms 5553723339")
        return

    gsm_number = user_input[1]
    api_url = f'http://172.208.52.218/api/legaliapi/smsvip.php?number={gsm_number}&adet=200'

    
    start_message = bot.send_message(chat_id, "Smsler Gönderiliyor...")

    
    response = requests.get(api_url)

    if response.status_code == 200:
        
        bot.send_message(chat_id, "Smsler Başarılı Bir Şekilde Gönderildi!")
    else:
        bot.send_message(chat_id, "SMS gönderirken bir hata oluştu.")

@bot.message_handler(commands=['yaz'])
def yaz_command(message):
    try:
        
        text = message.text.replace('/yaz ', '')

        
        formatted_text = text.replace(' ', '%20')

        
        api_url = f'http://apis.xditya.me/write?text={formatted_text}'

        
        response = requests.get(api_url)

        if response.status_code == 200:
            
            bot.send_photo(message.chat.id, photo=("dijvarhack.jpg", response.content))
        else:
            bot.reply_to(message, 'yarrami ye.')

    except Exception as e:
        bot.reply_to(message, 'sg')

@bot.message_handler(commands=['adsoyad'])
def sorgu(message):
    text = message.text
    if not text:
        bot.send_message(message.chat.id, "Geçersiz komut. Lütfen doğru formatta komut girin.")
        return

    words = text.split()
    isim = None
    isim2 = None
    soyisim = None
    il = None
    ilce = None
    for i in range(len(words)):
        if words[i] == "-isim" and i < len(words) - 1:
            isim = words[i + 1]
        elif words[i] == "-isim2" and i < len(words) - 1:
            isim2 = words[i + 1]
        elif words[i] == "-soyisim" and i < len(words) - 1:
            soyisim = words[i + 1]
        elif words[i] == "-il" and i < len(words) - 1:
            il = words[i + 1]
        elif words[i] == "-ilce" and i < len(words) - 1:
            ilce = words[i + 1]
    if not isim or not soyisim:
        text = "Yanlış Kullanım Yapıldı!\n -> /adsoyad  -isim ramazan -soyisim öztürk -il istanbul"
        bot.send_message(message.chat.id, text)
        return
    user_id = message.from_user.id
    user_name = message.from_user.first_name
 
    bot.send_message(user_id, f"*APİ'ye istek gönderildi çıkan sonuca göre uzun sürebilir. Eğer sonuç uzunsa size metin dosyası yoluyla iletilecektir.*", parse_mode="Markdown")
   
    if isim2:
        isim_birlestirmesi = urllib.parse.quote(f"{isim} {isim2}")
    else:
        isim_birlestirmesi = urllib.parse.quote(isim)
    if il and ilce:
        AdSoyadApisi_url = f"http://172.208.52.218/api/legaliapi/adsoyadililce.php?ad={isim_birlestirmesi}&soyad={soyisim}&il={il}&ilce={ilce}"
    elif il:
        AdSoyadApisi_url = f"http://172.208.52.218/api/legaliapi/adsoyadilvip.php?ad={isim_birlestirmesi}&soyad={soyisim}&il={il}"
    else:
        AdSoyadApisi_url = f"http://172.208.52.218/api/legaliapi/adsoyadvip.php?ad={isim_birlestirmesi}&soyad={soyisim}"
    response = requests.get(AdSoyadApisi_url)
    data = response.json()
    if data["success"] == "true":
        number = data["number"]
        if number > 0:
            people = data["data"]
            with open('sonuclar.txt', 'w', encoding='utf-8') as file:
                for person in people:
                    tc = person["TC"]
                    ad = person["ADI"]
                    soyad = person["SOYADI"]
                    dogumtarihi = person["DOGUMTARIHI"]
                    nufusil = person["NUFUSIL"]
                    nufusilce = person["NUFUSILCE"]
                    anneadi = person["ANNEADI"]
                    annetc = person["ANNETC"]
                    babaadi = person["BABAADI"]
                    babatc = person["BABATC"]
                    uyrugu = person["UYRUK"]
                    info = f"""
╭━━━━━━━━━━━━━╮
┃➥ [ + ] Sorgu Başarılı
┃➥ Adı: {ad}
┃➥ Soyadı: {soyad}
┃➥ T.C Kimlik Numarası: {tc}
┃➥ Doğum Tarihi: {dogumtarihi}
┃➥ Nüfus il: {nufusil}
┃➥ Nüfus ilçe: {nufusilce}
┃➥ Uyruk: {uyrugu}
╰━━━━━━━━━━━━━╯
╭━━━━━━━━━━━━━╮
┃➥ Anne Adı: {anneadi}
┃➥ Anne T.C: {annetc}
╰━━━━━━━━━━━━━╯
╭━━━━━━━━━━━━━╮
┃➥ Baba Adı: {babaadi}
┃➥ Baba T.C: {babatc}
╰━━━━━━━━━━━━━╯"""
                    file.write(info + "\n\n")
            with open('sonuclar.txt', 'rb') as file:
                bot.send_document(message.chat.id, file)
        else:
            time.sleep(1)
            bot.send_message(message.chat.id, "Veri Bulunamadı.")
    else:
        time.sleep(1)
        bot.send_message(message.chat.id, "Data bulunamadı.")


def create_response_text(api_data):
    response_text = (
        f"╭━━━━━━━━━━━━━╮\n"
        f"┃➥ [ + ] Sorgu Başarılı\n"
        f"╰━━━━━━━━━━━━━╯\n"
        f"╭━━━━━━━━━━━━━━\n"
        f"┃➥TC: {api_data.get('TC', '')}\n"
        f"┃➥ ADI: {api_data.get('ADI', '')}\n"
        f"┃➥ SOY ADI: {api_data.get('SOYADI', '')}\n"
        f"┃➥ DOĞUM TARİHİ: {api_data.get('DOGUMTARIHI', '')}\n"
        f"┃➥ İL: {api_data.get('NUFUSIL', '')}\n"
        f"┃➥ İLÇE: {api_data.get('NUFUSILCE', '')}\n"
        f"┃➥ ANNE ADI: {api_data.get('ANNEADI', '')}\n"
        f"┃➥ ANNE TC: {api_data.get('ANNETC', '')}\n"
        f"┃➥ BABA ADI: {api_data.get('BABAADI', '')}\n"
        f"┃➥ BABA TC: {api_data.get('BABATC', '')}\n"
        f"┃➥ UYRUK: {api_data.get('UYRUK', '')}\n"
        f"╰━━━━━━━━━━━━━━"
    )

    return response_text  

TCGSM_API = "https://sowixapi.online/api/sowixapi/tcgsm.php?tc="

@bot.message_handler(commands=['tcgsm'])
def handle_tcgsm(message):

    user_id = message.from_user.id
    user_name = message.from_user.first_name
 
    bot.send_message(user_id, f"İşleminiz Gerçekleştiriliyor, Lütfen Bekleyin...", parse_mode="Markdown")
    try:
        
        tc_number = message.text.split()[1]

        
        api_response = requests.get(TCGSM_API + tc_number).json()

        
        if api_response.get("success") == "true" and api_response.get("number") > 0:
            data = api_response.get("data")[0]
            gsm = data.get("GSM")
            tc = data.get("TC")

            
            result_text = f"╭━━━━━━━━━━━━━╮\n┃➥ GSM: {gsm}\n┃➥ TC: {tc}\n╰━━━━━━━━━━━━━╯"
            bot.send_message(message.chat.id, result_text)
        else:
           
            bot.send_message(message.chat.id, "Data bulunamadı.")
    except IndexError:
        time.sleep(1)
        bot.send_message(message.chat.id, "Lütfen geçerli bir TC numarası girin.")

GSRTC_API = "https://allahpro.online/apiler/fulgsm.php?gsm="


@bot.message_handler(commands=['gsmtc'])
def handle_gsmtc(message):
    
    user_id = message.from_user.id
    user_name = message.from_user.first_name
 
    bot.send_message(user_id, f"İşleminiz Gerçekleştiriliyor, Lütfen Bekleyin...", parse_mode="Markdown")
    try:
        # Extract GSM number from the command
        gsm_number = message.text.split()[1]

        
        api_response = requests.get(GSRTC_API + gsm_number).json()

        
        if api_response.get("success") == "true" and api_response.get("number") > 0:
            data = api_response.get("data")
            
            
            result_text = "╭━━━━━━━━━━━━━╮\n"
            for entry in data:
                tc = entry.get("TC")
                gsm = entry.get("GSM")
                result_text += f"┃➥ GSM: {gsm}\n┃➥ TC: {tc}\n╰━━━━━━━━━━━━━╯\n"

            
            bot.send_message(message.chat.id, result_text)
        else:
            
            bot.send_message(message.chat.id, "Data bulunamadı.")
    except IndexError:
        
        bot.send_message(message.chat.id, "Lütfen geçerli bir GSM numarası girin Başında 0 Olmadan.")



@bot.message_handler(commands=['iban'])
def iban_sorgula(message):
  
    
    user_id = message.from_user.id
    user_name = message.from_user.first_name
 
    bot.send_message(user_id, f"İşleminiz Gerçekleştiriliyor, Lütfen Bekleyin...", parse_mode="Markdown")
    
    chat_id = message.chat.id
    user_input = message.text.split(' ', 1)

    if len(user_input) != 2:
        bot.send_message(chat_id, "Lütfen Geçerli IBAN Girin Birleşik Şekilde.")
        return

    iban = user_input[1]
    api_url = f'https://sowixapi.online/api/sowixapi/iban.php?iban={iban}'

    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        if 'BANKA' in data and 'ŞUBE' in data:
            banka = data['BANKA']
            sube = data['ŞUBE']
            
            response_message = (
                "╭━━━━━━━━━━━━━╮\n"
                "┃➥ Banka Bilgileri\n"
                f"┃➥ ADI: {banka['Adı']}\n"
                f"┃➥ KOD: {banka['Kod']}\n"
                f"┃➥ SWİFT: {banka['Swift']}\n"
                f"┃➥ HESAP NO: {banka['Hesap No']}\n"
                "╰━━━━━━━━━━━━━╯\n\n"
                "╭━━━━━━━━━━━━━╮\n"
                "┃➥ Şube Bilgileri\n"
                f"┃➥ ADI: {sube['Ad']}\n"
                f"┃➥ KOD: {sube['Kod']}\n"
                f"┃➥ İL: {sube['İl']}\n"
                f"┃➥ İLÇE: {sube['İlçe']}\n"
                f"┃➥ TEL: {sube['Tel']}\n"
                f"┃➥ FAX: {sube['Fax']}\n"
                f"┃➥ ADRES: {sube['Adres']}\n"
                "╰━━━━━━━━━━━━━╯"
            )

            bot.send_message(chat_id, response_message)

                        
        else:
            bot.send_message(chat_id, "𝖲𝗈𝗇𝗎𝖼̧ 𝖡𝗎𝗅𝗎𝗇𝗆𝖺𝖽ı.")
    else:
        bot.send_message(chat_id, "Data bulunamadı.")

TC_API = "https://sowixapi.online/api/sowixapi/tcpro.php?tc="


@bot.message_handler(commands=['tc'])  
def handle_tc_command(message):
    
    user_id = message.from_user.id
    user_name = message.from_user.first_name
 
    bot.send_message(user_id, f"İşleminiz Gerçekleştiriliyor, Lütfen Bekleyin...", parse_mode="Markdown")
    try:
        
        tc = message.text.split()[1]
        
        
        api_response = requests.get(TC_API + tc).json()

        
        adi = api_response.get("ADI", "")
        soyadi = api_response.get("SOYADI", "")
        dogum_tarihi = api_response.get("DOĞUMTARIHI", "")
        il = api_response.get("NUFUSIL", "")
        ilce = api_response.get("NUFUSILCE", "")
        anne_adi = api_response.get("ANNEADI", "")
        anne_tc = api_response.get("ANNETC", "")
        baba_adi = api_response.get("BABAADI", "")
        baba_tc = api_response.get("BABATC", "")
        yas = api_response.get("YAŞ", "")

        
        response_text = (
            f"╭━━━━━━━━━━━━━━\n"
            f"┃➥ TC: {tc}\n"
            f"┃➥ ADI: {adi}\n"
            f"┃➥ SOY ADI: {soyadi}\n"
            f"┃➥ DOĞUM TARİHİ: {dogum_tarihi}\n"
            f"┃➥ İL: {il}\n"
            f"┃➥ İLÇE: {ilce}\n"
            f"┃➥ ANNE ADI: {anne_adi}\n"
            f"┃➥ ANNE TC: {anne_tc}\n"
            f"┃➥ BABA ADI: {baba_adi}\n"
            f"┃➥ BABA TC: {baba_tc}\n"
            f"┃➥ YAŞ: {yas}\n"
            f"╰━━━━━━━━━━━━━━"
        )

        
        bot.reply_to(message, response_text)

    except IndexError:
       
        bot.reply_to(message, "Geçerli Bir TC Kimlik Numarası Girin.")
    except Exception as e:
        time.sleep(1)
        bot.reply_to(message, f"Data bulunamadı.")


AILE_API = "https://sowixapi.online/api/sowixapi/aile.php?tc="

@bot.message_handler(commands=['aile'])
def handle_aile_command(message):
    
    user_id = message.from_user.id
    user_name = message.from_user.first_name
 
    bot.send_message(user_id, f"İşleminiz Gerçekleştiriliyor, Lütfen Bekleyin...", parse_mode="Markdown")
        
    try:
        
        tc = message.text.split()[1]
        
        
        api_response = requests.get(AILE_API + tc).json()

        
        user_info = api_response.get("data", [])

        time.sleep(1)
        response_text = (
            f""
            f""
            f""
        )

        for info in user_info:
            response_text += (
                f"\n"
                f"╭━━━━━━━━━━━━━━\n"
                f"┃➥ TC: {info['TC']}\n"
                f"┃➥ ADI: {info['ADI']}\n"
                f"┃➥ SOY ADI: {info['SOYADI']}\n"
                f"┃➥ DOĞUM TARİHİ: {info['DOGUMTARIHI']}\n"
                f"┃➥ İL: {info['NUFUSIL']}\n"
                f"┃➥ İLÇE: {info['NUFUSILCE']}\n"
                f"┃➥ ANNE ADI: {info['ANNEADI']}\n"
                f"┃➥ ANNE TC: {info['ANNETC']}\n"
                f"┃➥ BABA ADI: {info['BABAADI']}\n"
                f"┃➥ BABA TC: {info['BABATC']}\n"
                f"┃➥ UYRUK: {info['UYRUK']}\n"
                f"┃➥ YAKINLIK: {info['Yakinlik']}\n"
                f"╰━━━━━━━━━━━━━━"
            )

        
        bot.reply_to(message, response_text)

    except IndexError:
        
        bot.reply_to(message, "Lütfen geçerli bir TC kimlik numarası girin.")
    except Exception as e:
        
        bot.reply_to(message, f"Bilgiler Bulunamadı")


@bot.message_handler(commands=["kizlik"])
def kizlik(message):
    
    user_id = message.from_user.id
    user_name = message.from_user.first_name
 
    bot.send_message(user_id, f"İşleminiz Gerçekleştiriliyor, Lütfen Bekleyin...", parse_mode="Markdown")
        
    try:
        tc = message.text.split()[1]
        api_url = f"http://172.208.52.218/api/legaliapi/kizlik.php?tc={tc}"
        response = requests.get(api_url).json()
        time.sleep(1)
        output = f"""
╔═══════════════
╟ TC: {response["TC"]}
╟ İSİM: {response["ADI"]}
╟ SOY ADI: {response["SOYADI"]}
╟ DOĞUM TARİHİ: {response["DOGUMTARIHI"]}
╟ KIZLIK SOY: {response["KIZLIKSOYADI"]}
╟ İL: {response["NUFUSIL"]}
╟ GSM: {response["KENDI_GSM"][0]["GSM"]}
╟ ANNE ADI: {response["ANNEADI"]}
╟ ANNE GSM: {response["ANNE_GSM"][0]["GSM"]}
╟ BABA ADI: {response["BABAADI"]}
╟ BABA GSM: {response["BABA_GSM"][0]["GSM"]}
╟ ANNE TC: {response["ANNETC"]}
╟ BABA TC: {response["BABATC"]}
╟ YAŞ: {response["YAS"]}
╟ KURUM KODU: Bilinmiyor
╚═══════════════
"""
        bot.send_message(message.chat.id, output)
    except IndexError:
        
        bot.send_message(message.chat.id, "Lütfen Geçerli Bir TC Kimlik Numarası Girin.")
    except Exception as e:
        
        bot.send_message(message.chat.id, f"Data bulunamadı.")
        
@bot.message_handler(commands=["adres"])
def adres(message):     
 user_id = message.from_user.id
 user_name = message.from_user.first_name
 
 bot.send_message(user_id, f"İşleminiz Gerçekleştiriliyor, Lütfen Bekleyin...", parse_mode="Markdown")
 try:
  tc = message.text.split(' ')[1]
  he=requests.get(f"https://sowixapi.online/api/sowixapi/adres.php?tc={tc}").json()
  tc = he["data"]["KimlikNo"]
  adisoyadi = he["data"]["AdSoyad"]
  dogum_yeri = he["data"]["DogumYeri"] 
  vergi_numarasi = he["data"]["VergiNumarasi"]
  adres = he["data"]["Ikametgah"]
  
  
  text = f'''
╔═══════════════
╟ TC: {tc}
╟ ADI: {adisoyadi}
╟ DOĞUM YERİ: {dogum_yeri}
╟ VERGİ NUMARASI: {vergi_numarasi}
╟ ADRES: {adres}
╚═══════════════
'''
 
  bot.send_message(message.chat.id,text)
 except IndexError:
  
  text = '''
Geçerli bir tc girmediniz!'''
  bot.send_message(message.chat.id, text)
 except:
  
  text = '''
Data bulunamadı.'''
  bot.send_message(message.chat.id, text)

@bot.message_handler(commands=["operator"])
def operator_command(message):
    
     
    user_id = message.from_user.id
    user_name = message.from_user.first_name
 
    bot.send_message(user_id, f"İşleminiz Gerçekleştiriliyor, Lütfen Bekleyin...", parse_mode="Markdown")
    try:
        gsm = message.text.split()[1]
        api_url = f"https://legendofbozkurt.icu/bozkurtramo/operator.php?gsm={gsm}"
        response = requests.get(api_url).json()
        
        output = f"""
╭━━━━━━━━━━━━━╮
┃➥ GSM: {response["gsm"]}
┃➥ OPRT: {response["operator"]}
╰━━━━━━━━━━━━━╯
"""
        bot.send_message(message.chat.id, output)
    except IndexError:
        
        bot.send_message(message.chat.id, "Lütfen geçerli bir GSM numarası girin.")
    except Exception as e:
        
        bot.send_message(message.chat.id, f"Data bulunamadı.")


@bot.message_handler(commands=["vergid"])
def vergidairesi(message):
    
    user_id = message.from_user.id
    user_name = message.from_user.first_name
 
    bot.send_message(user_id, f"İşleminiz Gerçekleştiriliyor, Lütfen Bekleyin...")
    try:
        tc = message.text.split()[1]
        api_url = f"http://172.208.52.218/api/legaliapi/vergid.php?tc={tc}"
        response = requests.get(api_url).json()
        
        output = f"""
╔═══════════════
╟ TC: {response["tc"]}
╟ ADI: {response["adi"]}
╟ SOYADI: {response["soyadi"]}
╟ VERGİ DAİRESİ: {response["vergi dairesi"]}
╚═══════════════
"""
        bot.send_message(message.chat.id, output)
    except IndexError:
        
        bot.send_message(message.chat.id, "Lütfen Geçerli Bir TC Kimlik Numarası Girin.")
    except Exception as e:
        
        bot.send_message(message.chat.id, f"Data bulunamadı.")

@bot.message_handler(commands=["burc"])
def burc(message):
    
    user_id = message.from_user.id
    user_name = message.from_user.first_name
 
    bot.send_message(user_id, f"İşleminiz Gerçekleştiriliyor, Lütfen Bekleyin...", parse_mode="Markdown")
        
    try:
        tc = message.text.split()[1]
        api_url = f"https://sowixapi.online/api/sowixapi/burc.php?tc={tc}"
        response = requests.get(api_url).json()
        
        output = f"""
╔═══════════════
╟ TC: {response["TC"]}
╟ İSİM: {response["ADI"]}
╟ SOYİSİM: {response["SOYADI"]}
╟ BURC: {response["BURC"]}
╚═══════════════
"""
        bot.send_message(message.chat.id, output)
    except IndexError:
        
        bot.send_message(message.chat.id, "Lütfen Geçerli Bir TC Kimlik Numarası Girin.")
    except Exception as e:
        
        bot.send_message(message.chat.id, f"Data bulunamadı.")        
                        

@bot.message_handler(commands=["sicil"])
def sicil_command(message):
    
    user_id = message.from_user.id
    user_name = message.from_user.first_name
 
    bot.send_message(user_id, f"İşleminiz Gerçekleştiriliyor, Lütfen Bekleyin...", parse_mode="Markdown")
        
    try:
        tc = message.text.split()[1]
        api_url = f"https://sowixapi.online/api/sowixapi/sicil.php?tc={tc}"
        response = requests.get(api_url).json()
        
        result = response[0]  
        
        output = f"""
╔═══════════════
╟ TC: {result["KIMLIKNO"]}
╟ ADI: {result["ISIM"]}
╟ SOY ADI: {result["SOYISIM"]}
╟ SAYI: {result["SAYI"]}
╟ S. TÜRÜ: {result["SORGUTURU"]}
╟ K. TÜRÜ: {result["KIMLIKTURU"]}
╟ SİCİL: {result["SICILKAYIT"]}
╟ İŞLENEN YER: {result["SICILINISLENDIGIYER"]}
╚═══════════════
"""
        bot.send_message(message.chat.id, output)
    except IndexError:
        
        bot.send_message(message.chat.id, "Lütfen geçerli bir TC kimlik numarası girin.")
    except Exception as e:
        
        bot.send_message(message.chat.id, f"Data bulunamadı.")
        
@bot.message_handler(commands=['kban'])
def kban_command(message):

    if message.chat.id != bot_owner_chat_id:
        bot.send_message(message.chat.id, "Bu komutu kullanmak için bot sahibi olmanız gerekiyor.")
        return

    chat_id = message.chat.id
    user_message = message.text.split()

    if len(user_message) == 1:
        bot.send_message(chat_id, "Lütfen Komutu Doğru Kullanın. Örnek: /kban <id> veya /kban <id> <sebep>")
    else:
        banned_user_id = user_message[1]
        ban_reason = user_message[2] if len(user_message) > 2 else "Sebepsiz"
        ban_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(banned_users_file, "a") as file:
            file.write(f"{banned_user_id} {ban_date} {ban_reason}\n")

        reply_text = f"Kullanıcı Yasaklandı!\nID: {banned_user_id}\nSEBEP: {ban_reason}"
        bot.send_message(chat_id, reply_text)

@bot.message_handler(commands=['unkban'])
def unkban_command(message):

    if message.chat.id != bot_owner_chat_id:
        bot.send_message(message.chat.id, "Bu komutu kullanmak için bot sahibi olmanız gerekiyor.")
        return
    chat_id = message.chat.id
    user_message = message.text.split()

    if len(user_message) == 1:
        bot.send_message(chat_id, "Lütfen Komutu Doğru Kullanın. Örnek: /unkban <id>")
    else:
        unbanned_user_id = user_message[1]

        with open(banned_users_file, "r") as file:
            lines = file.readlines()

        with open(banned_users_file, "w") as file:
            for line in lines:
                if unbanned_user_id not in line:
                    file.write(line)

        reply_text = f"Kullanıcının Yasağı Kaldırıldı! Tekrardan Hizmet Sağlanacak!"
        bot.send_message(chat_id, reply_text)

@bot.message_handler(commands=['start', 'tc', 'aile', 'tcgsm', 'gsmtc', 'tcv2', 'sicil', 'serino', 'cm', 'sorgu', 'operator', 'adres', 'vergid', 'tcplaka', 'plakaborc', 'okulno', 'kizlik', 'burc', 'ip', 'iban', 'ayakno', 'index', 'gpt', 'yaz', 'tekrarla', 'yenilikler', 'destek'])
def restricted_commands(message):
    chat_id = message.chat.id
    user_id = str(message.from_user.id)

    if user_id in get_banned_users():
        bot.send_message(chat_id, "Üzgünüm, TelethonUserbot Yasaklı Üyesiniz. Size Hizmet Sağlayamam!\n\nYasağın Yanlışlıkla Olduğunu Düşünüyorsanız Destek Grubumuz Olan @DARKFLESHCHAT Gelin!")

@bot.message_handler(func=lambda message: True, content_types=['text'], regexp=".+")
def banned_user_response(message):
    chat_id = message.chat.id
    user_id = str(message.from_user.id)

    if user_id in get_banned_users():
        bot.send_message(chat_id, "Üzgünüm, Legend Arsiv Yasaklı Üyesiniz. Size Hizmet Sağlayamam!\n\nYasağın Yanlışlıkla Olduğunu Düşünüyorsanız Destek Grubumuz Olan @DARKFLESHCHAT Gelin!")

def get_banned_users():
    with open(banned_users_file, "r") as file:
        lines = file.readlines()
    return [line.split()[0] for line in lines] 
            
                                  
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(f"Hata: {e}")
