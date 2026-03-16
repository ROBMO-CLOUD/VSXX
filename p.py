from telethon import TelegramClient, events
import telebot
import re
import datetime
import asyncio
import random
from time import sleep
from os import system, name, execv
from sys import executable, argv
from bin import get_bin_info
from apis import apid, apihasd, token

now = datetime.datetime.now()
mes_actual = now.month
ano_actual = now.year

client = TelegramClient('scrapfree', apid, apihasd)
client.parse_mode = 'html'
bot = telebot.TeleBot(token, parse_mode="html")
id_channel = -1002450247913
id_alert_channel = -1002432179007

keywords = ['Card Issuer Declined CVV', 'Approved! ✅', 'Approved', 'Card Issuer Declined CVV', '1000: Approved', 'CVC Declined ', 'CVV2 DECLINED', '𝒔𝒖𝒄𝒄𝒆𝒆𝒅𝒆𝒅', '𝑹𝒆𝒔𝒑𝒐𝒏𝒔𝒆 -» 𝑨𝒑𝒑𝒓𝒐𝒗𝒆𝒅', ' CVV_NOT_PROCESSED', 'Request was processed successfully.', 'Invalid Card Verification Number (CVN)', 'succeeded', 'DECLINED CVV2', 'Gateway Rejected: cvv', "Your card's security code is incorrect", '1000 Approved', 'Insufficient Funds', 'Your card has insufficient funds', 'Gateway Rejected: avs_and_cvv', 'Verified', 'CVV_MATCHED']

keywords_dec = None

cards_process = {}

def vef_ccn(ccn):
    with open('ccs.txt', 'r') as f:
        r = f.read()
    return ccn in r

async def handle_login_issue():
    message = "El bot necesita iniciar sesión nuevamente. Verifica si es necesario."
    try:
        await bot.send_message(id_alert_channel, message)
    except Exception as e:
        print(f"Error: {e}")

@client.on(events.NewMessage)
async def edited_event(event: events):
    global keywords_dec
    try:
        edited_text = event.raw_text
    except MemoryError:
        return ...

    card_pattern = re.compile(r'\b(\d{16})\|(\d{2})\|(\d{4})\|(\d{3})\b')
    x = card_pattern.findall(edited_text)

    try:
        cc = x[0][0]
        mes = x[0][1]
        ano = x[0][2]
        cvv = x[0][3]

        if cards_process.get(cc, 0) >= 3:
            return

        if not vef_ccn(cc):
            for _ in range(4):
                    random_digits = "".join(random.choice("0123456789") for _ in range(6))
                    random_month = random.randint(1, 12)
                    random_year = random.randint(2025, 2030)

            x = get_bin_info(cc[:6])

            text = f"""<b><a href="https://raw.githubusercontent.com/VSXX-SCRP/Code/main/scrp.jpg">&#8203;</a>
[<a href="https://t.me/+CqNAreUKC_tiYzFh">么</a>] 𝐕𝐒𝐗𝐗 𝐒𝐂𝐑𝐀𝐏𝐏𝐄𝐑  - 【 𝐅𝐑𝐄𝐄 】 
━━━━━━━━━━━━━━━━
[<a href="https://t.me/+CqNAreUKC_tiYzFh">么</a>] #bin{cc[:6]}
━━━━━━━━━━━━━━━━
[<a href="https://t.me/+CqNAreUKC_tiYzFh">么</a>] CC ➫ <code>{cc}|{mes}|{ano}|{cvv}</code>
━━━━━━━━━━━━━━━━
[<a href="https://t.me/+CqNAreUKC_tiYzFh">么</a>] Country ➫ <code>{x.get("country")}</code> | <code>{x.get("flag")}</code>
[<a href="https://t.me/+CqNAreUKC_tiYzFh">么</a>] Type ➫ <code>{x.get("type")}</code> | <code>{x.get("vendor")}</code>
[<a href="https://t.me/+CqNAreUKC_tiYzFh">么</a>] Level ➫ <code>{x.get("level")}</code>
[<a href="https://t.me/+CqNAreUKC_tiYzFh">么</a>] Bank ➫ <code>{x.get("bank_name")}</code> 
━━━━━━━━━━━━━━━━
[<a href="https://t.me/+CqNAreUKC_tiYzFh">么</a>] Extra ➫ <code>{cc[:6]}{random_digits}xxxx|{random_month:02d}|{random_year}|rnd</code>
[<a href="https://t.me/+CqNAreUKC_tiYzFh">么</a>] Powered by ➫ <a href="https://t.me/CL0UD_ADMIN">@CL0UD_ADMIN 🥀</a>
‎ ‎ 
    </b>"""

            sleep(31.5)
            try:
                bot.send_message(
                    id_channel, 
                    text, 
                    parse_mode="HTML",
                    )
            except:
                bot.send_message(id_channel, text, disable_web_page_preview=True)

            cards_process[cc] = cards_process.get(cc, 0) + 1

            with open('ccs.txt', 'a') as f:
                f.write(cc + '\n')

    except:
        pass

system('cls' if name == 'nt' else 'clear')
print('@CL0UD_ADMIN')

try:
    client.start()
except Exception as e:
    print(f"Error: {e}")
    asyncio.run(handle_login_issue())  

client.run_until_disconnected()
