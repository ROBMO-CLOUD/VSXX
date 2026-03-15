import re
import asyncio
import random
import telebot
from telethon import TelegramClient, events
from os import system, name
from bin import get_bin_info
from apis import apid, apihasd, token

# --- CONFIGURACIÓN ---
client = TelegramClient('scrapfree', apid, apihasd)
bot = telebot.TeleBot(token, parse_mode="html")

id_channel = -1002450247913
id_alert_channel = -1002432179007

# Usamos un set en memoria para evitar duplicados sin usar archivos .txt
processed_ccs = set()
cards_process_count = {}

# --- LÓGICA DE PROCESAMIENTO ---

async def process_card(cc, mes, ano, cvv):
    """Tarea independiente para cada tarjeta"""
    # Evitar procesar la misma CC más de 3 veces en la sesión actual
    if cards_process_count.get(cc, 0) >= 3:
        return
    
    # Marcamos como procesada para evitar duplicados inmediatos
    processed_ccs.add(cc)
    
    # Simulamos el delay de 31.5s sin bloquear a los demás chats
    await asyncio.sleep(31.5)

    try:
        bin_data = get_bin_info(cc[:6])
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
[<a href="https://t.me/+CqNAreUKC_tiYzFh">么</a>] Country ➫ <code>{bin_data.get("country")}</code> | <code>{bin_data.get("flag")}</code>
[<a href="https://t.me/+CqNAreUKC_tiYzFh">么</a>] Type ➫ <code>{bin_data.get("type")}</code> | <code>{bin_data.get("vendor")}</code>
[<a href="https://t.me/+CqNAreUKC_tiYzFh">么</a>] Level ➫ <code>{bin_data.get("level")}</code>
[<a href="https://t.me/+CqNAreUKC_tiYzFh">么</a>] Bank ➫ <code>{bin_data.get("bank_name")}</code> 
━━━━━━━━━━━━━━━━
[<a href="https://t.me/+CqNAreUKC_tiYzFh">么</a>] Extra ➫ <code>{cc[:6]}{random_digits}xxxx|{random_month:02d}|{random_year}|rnd</code>
[<a href="https://t.me/+CqNAreUKC_tiYzFh">么</a>] Powered by ➫ <a href="https://t.me/CL0UD_ADMIN">@CL0UD_ADMIN 🥀</a>
</b>"""

        try:
            bot.send_message(id_channel, text)
        except Exception:
            bot.send_message(id_channel, text, disable_web_page_preview=True)

        cards_process_count[cc] = cards_process_count.get(cc, 0) + 1

    except Exception as e:
        print(f"Error procesando {cc}: {e}")

@client.on(events.NewMessage)
async def main_handler(event):
    if not event.raw_text:
        return

    # Regex que busca el formato CC|MES|AÑO|CVV
    card_pattern = re.compile(r'\b(\d{16})\|(\d{2})\|(\d{4})\|(\d{3})\b')
    matches = card_pattern.findall(event.raw_text)

    for match in matches:
        cc, mes, ano, cvv = match
        
        # Filtro de duplicados en memoria
        if cc in processed_ccs and cards_process_count.get(cc, 0) >= 1:
            continue

        # Lanza la tarea al fondo y sigue escuchando otros chats
        asyncio.create_task(process_card(cc, mes, ano, cvv))

async def main():
    system('cls' if name == 'nt' else 'clear')
    print('--- SCRAPER ACTIVO (SIN TXT / MULTITAREA) ---')
    print('@CL0UD_ADMIN')
    
    await client.start()
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
