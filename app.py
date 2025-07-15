from fastapi import FastAPI, Request , Query
import base64
import datetime
from fastapi.responses import FileResponse
import os, requests


app = FastAPI()

MAIL_TOKEN = "8113524955:AAEQovNmZr-38ogi3UQBgrC20rNtwIslJ_c"
EME = "7890080421:AAFs4eXADn47TTFzhkjKSVsKgP8-2TYBNcw"

CON_BOT_TOKEN = "7682957953:AAE_UVOfIFKNQ3dMANjsH6JMwLTAbocI8ys"
CON_CHAT_ID = "5660125152"

PRE_BOT_TOKEN = "7228712143:AAGjZXlM_i2nNI6xsTvRgbokge1o9lQjf-8"
PRE_CHAT_ID = "5660125152"

ALEX_BOT_TOKEN = "8020725694:AAHVb-njS2E9cTWmZXdNxUjBq3m58tlFH_A"
ALEX_CHAT_ID = "5660125152"

OTHER_BOT_TOKEN = "7399814752:AAGI-IAMNxImH6ATsY3T3iRf8Y1EAvn-7F0"
OTHER_CHAT_ID = "5660125152"

def send_telegram(token, chat_id, message):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message}
    requests.post(url, data=payload)


def formatt_order_message(order):
    order_number = order.get("order_number")
    total_price = order.get("total_price") + " EGP"

    note_attrs = order.get("note_attributes", [])
    phone = ""
    for attr in note_attrs:
        if attr.get("name") == "Whatsapp number (IMPORTANT)":
            phone = attr.get("value", "").replace("+", "").replace(" ", "")
            break

    phone1 = order.get("shipping_address", {}).get("phone", "").replace("+", "").replace(" ", "")
    address1 = order.get("shipping_address", {}).get("address1", "")
    name = order.get("shipping_address", {}).get("name", "")

    line_items = order.get("line_items", [])
    products = ""
    for item in line_items:
        if item['title'] =="Cash on Delivery fee" or item['title'] =='Normal Package' or item['title'] =='Premium Package':
            continue
        else:
            products += f"- {item['title']} (x{item['quantity']})\n"

    

    

    msg1 = f"""Whatsapp number = {phone}
phone number= {phone1}

Hi {name}

안녕하세요!  to Korean Beautys   🌸  

بنتواصل مع حضرتك لتأكيد طلبك رقم 007{order_number}

بمبلغ {total_price}

عنوان: {address1}


{products}📦 الطلب هيتم شحنه غدا وهيوصل خلال ٢-٥ ايام  من يوم التأكيد  


📌 ملحوظة مهمة:  
•⁠  ⁠بعد شحن الطلب، لا يمكن إلغاؤه.  
•⁠في حالة الإلغاء بعد الشحن، يتم تحصيل مصاريف الشحن85 جنيه لكل المحافظات من حضرتك .  

•⁠  ⁠الطلب له محاولتان للتوصيل، والتوصيل يكون من الساعة 10 صباحًا حتى 7 مساءًا

•⁠  ⁠في حال تغيير العنوان بعد الشحن، يستغرق التعديل 48 ساعة عمل.  

•⁠  ⁠في حال كان العنوان غير واضح، يُرجى تحديده بدقة بذكر (المحافظة – المنطقة – أقرب معلم واضح) لتجنب أي تأخير في التوصيل.   

🎁 خصم 3% على أوردر حضرتك عند الدفع قبل الشحن!

💳 طرق الدفع المتاحة:

⿡ InstaPay  تحويل لحساب بنكي: فقط 
01066350652

⿢ Vodafone Cash – من خلال إرسال الفاتورة:
هنبعتلك فاتورة الدفع على الإيميل، وتقدر تسدد مباشرة منها.

📸 بعد الدفع، ابعتلنا صورة الإيصال، وهنبدأ إجراءات الشحن فورًا 💨
⚠ العرض متاح فقط للدفع قبل الشحن، والتحويل خلال 6–12 ساعة، وإلا هيتم إلغاء الأوردر تلقائيًا"""
    
    return msg1



def format_order_message(order):
    order_number = order.get("order_number")
    total_price = order.get("total_price") + " EGP"

    note_attrs = order.get("note_attributes", [])
    phone = ""
    for attr in note_attrs:
        if attr.get("name") == "Whatsapp number (IMPORTANT)":
            phone = attr.get("value", "").replace("+", "").replace(" ", "")
            break

    phone1 = order.get("shipping_address", {}).get("phone", "").replace("+", "").replace(" ", "")
    address1 = order.get("shipping_address", {}).get("address1", "")
    name = order.get("shipping_address", {}).get("name", "")

    line_items = order.get("line_items", [])
    products = ""
    for item in line_items:
        if item['title'] =="Cash on Delivery fee" or item['title'] =='Normal Package' or item['title'] =='Premium Package':
            continue
        else:
            products += f"- {item['title']} (x{item['quantity']})\n"

    

    

    msg = f"""Whatsapp number = {phone}
phone number= {phone1}

Hi {name}

안녕하세요!  to Korean Beautys   🌸  

بنتواصل مع حضرتك لتأكيد طلبك رقم 007{order_number}

بمبلغ {total_price}

عنوان: {address1}


{products}📦 الطلب هيتم شحنه غدا وهيوصل خلال ٢-٥ ايام  من يوم التأكيد  


📌 ملحوظة مهمة:  
•⁠  ⁠بعد شحن الطلب، لا يمكن إلغاؤه.  
•⁠في حالة الإلغاء بعد الشحن، يتم تحصيل مصاريف الشحن85 جنيه لكل المحافظات من حضرتك .  

•⁠  ⁠الطلب له محاولتان للتوصيل، والتوصيل يكون من الساعة 10 صباحًا حتى 7 مساءًا

•⁠  ⁠في حال تغيير العنوان بعد الشحن، يستغرق التعديل 48 ساعة عمل.  

•⁠  ⁠في حال كان العنوان غير واضح، يُرجى تحديده بدقة بذكر (المحافظة – المنطقة – أقرب معلم واضح) لتجنب أي تأخير في التوصيل.   

لو معندناش رد خلال 24 ساعة، الاوردر بيتلغي تلقائيًا."""
    
    return msg

@app.post("/webhook")
async def handle_order(request: Request):
    data = await request.json()
    paid = data.get("financial_status", "")
    codes = data.get("discount_codes", [])
    code_values = [c.get("code", "") for c in codes]
    codes_text = ", ".join(filter(None, code_values)) or "NO"
    
    if paid=="Paid" or paid=="paid":

        return {"status": "paid - skipped"}
    
    elif "PREPAID" in codes_text:
        message = formatt_order_message(data)
        send_telegram(PRE_BOT_TOKEN, PRE_CHAT_ID, message)
        return {"status": "sent to prepaid bot"}
    

    else:
        message = format_order_message(data)

        province = (
            data.get("shipping_address", {}).get("province_code", "") or
            data.get("billing_address", {}).get("province_code", "")
        ).lower()


        if "alx" in province:
            send_telegram(ALEX_BOT_TOKEN, ALEX_CHAT_ID, message)
        else:
            send_telegram(OTHER_BOT_TOKEN, OTHER_CHAT_ID, message)

        return {"status": "sent"}

@app.get("/confirm")
def notify_order(order_number: str):
    message = f"🔔 order: {order_number} has been delivered successfully"
    send_telegram(CON_BOT_TOKEN, CON_CHAT_ID, message)
    return {"status": "message sent", "order": order_number}


@app.post("/zoho-mail-webhook")
async def zoho_mail_webhook(req: Request):
    data = await req.json()

    sender = data.get("fromAddress", "Unknown Sender")
    subject = data.get("subject", "No Subject")
    summary = data.get("summary", "")
    
    message = f"""📧 New Email Received
From: {sender}
Subject: {subject}
Snippet: {summary}"""

    url = f"https://api.telegram.org/bot{MAIL_TOKEN}/sendMessage"
    payload = {
        "chat_id": OTHER_CHAT_ID,
        "text": message
    }
    requests.post(url, data=payload)
    
    return {"status": "Message sent to Telegram"}


@app.post("/bosta-webhook")
def handle_bosta_webhook(request: Request):
    data = request.json()
    
    state = data.get("state")
    tracking = data.get("trackingNumber")
    business_ref = data.get("businessReference", "")
    
    if state == 103:
        msg = f"📦 🦺Emergence🦺 \nTracking #: {tracking}\nBusiness Ref: {business_ref}\nStatus: Awaiting your action"
        send_telegram(EME, CON_CHAT_ID, msg)
        return {"status": "notified"}
    elif state == 100:
        msg = f"📦 🦺Emergence🦺 \nTracking #: {tracking}\nBusiness Ref: {business_ref}\nStatus: Package Lost"
        send_telegram(EME, CON_CHAT_ID, msg)
        return {"status": "notified"}
    elif state == 101:
        msg = f"📦 🦺Emergence🦺 \nTracking #: {tracking}\nBusiness Ref: {business_ref}\nStatus: Package Damaged"
        send_telegram(EME, CON_CHAT_ID, msg)
        return {"status": "notified"}
    else:
        return {"status": "ignored", "state": state}


last_tracking_number = None
last_order_name = None

BOSTA_TOKEN = "3df1df2a6ca817c65b3144ef2ad57f1290a87105e8faf6c28db88cdafd11b417"
BOSTA_URL = "https://app.bosta.co/api/v2/deliveries/mass-awb"

TELEGRAM_BOT_TOKEN = "7370583584:AAFOaJsnq5uYa-qWWjJlSbqfFvCHVaYbGTg"
TELEGRAM_CHAT_ID = "5660125152"

SHOP_NAME     = "korean-beauty-s"
API_VERSION   = "2024-07"
ACCESS_TOKEN  = "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"


@app.post("/tracking")
async def save_and_send_tracking(request: Request):
    global last_tracking_number, last_order_name

    data = await request.json()
    last_tracking_number = data.get("tracking_number", "")
    last_order_name = data.get("name", "").replace(".1", "")

    response_data = {
        "status": "stored",
        "tracking_number": last_tracking_number,
        "name": last_order_name
    }

    payload = {
        "trackingNumbers": last_tracking_number,
        "requestedAwbType": "A6",
        "lang": "en"
    }
    headers = {
        "Authorization": BOSTA_TOKEN
    }

    try:
        res = requests.post(BOSTA_URL, json=payload, headers=headers)
        res.raise_for_status()
        res_json = res.json()
        response_data["bosta_response"] = res_json

        base64_pdf = res_json.get("data")
        if base64_pdf:
            pdf_bytes = base64.b64decode(base64_pdf)
            filename = f"{last_order_name}.pdf"

            telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendDocument"
            files = {
                "document": (filename, pdf_bytes, "application/pdf")
            }
            telegram_data = {
                "chat_id": TELEGRAM_CHAT_ID,
                "caption": f"📄 AirwayBill for {last_order_name}"
            }

            telegram_response = requests.post(telegram_url, data=telegram_data, files=files)

            if telegram_response.status_code == 200:
                response_data["telegram_status"] = "sent"
            else:
                response_data["telegram_status"] = "failed"
                response_data["telegram_error"] = telegram_response.text
        else:
            response_data["error"] = "No base64 PDF found in Bosta response."

    except Exception as e:
        response_data["error"] = str(e)
        if "res" in locals():
            response_data["bosta_raw"] = res.text

    return response_data
