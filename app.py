from fastapi import FastAPI, Request , Query
import base64
import datetime
from fastapi.responses import FileResponse
import os, requests
from weasyprint import HTML , CSS
from cachetools import TTLCache

app = FastAPI()

MAIL_TOKEN = os.getenv("MAIL_TOKEN")
EME = os.getenv("EME")

CON_BOT_TOKEN = os.getenv("CON_BOT_TOKEN")
CON_CHAT_ID = os.getenv("CON_CHAT_ID")

PRE_BOT_TOKEN = os.getenv("PRE_BOT_TOKEN")
PRE_CHAT_ID = os.getenv("PRE_CHAT_ID")

ALEX_BOT_TOKEN = os.getenv("ALEX_BOT_TOKEN")
ALEX_CHAT_ID = os.getenv("ALEX_CHAT_ID")

OTHER_BOT_TOKEN = os.getenv("OTHER_BOT_TOKEN")
OTHER_CHAT_ID = os.getenv("OTHER_CHAT_ID")

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
    
    elif "Instapay" in data.get("payment_gateway_names", []):
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

BOSTA_TOKEN = os.getenv("BOSTA_TOKEN")
BOSTA_URL = os.getenv("BOSTA_URL")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OTHER_CHAT_ID = os.getenv("OTHER_CHAT_ID")

SHOP_NAME     = os.getenv("SHOP_NAME")
API_VERSION   = os.getenv("API_VERSION")
ACCESS_TOKEN  = os.getenv("ACCESS_TOKEN")

def send_invoice_to_telegram(order: dict, image_map: dict):
    subtotal        = float(order.get("current_subtotal_price", 0))
    total_discounts = float(order.get("current_total_discounts", 0))
    true_subtotal   = subtotal + total_discounts
    shipping_price  = 0
    shipping_lines  = order.get("shipping_lines", [])
    if shipping_lines:
        shipping_price = float(shipping_lines[0].get("price", 0))
    total_price     = float(order.get("current_total_price", 0))

    paid_amount = total_price if order.get("financial_status", "").lower() == "paid" else 0
    outstanding = total_price - paid_amount

    note = order.get("note", "")
    ship_addr = order.get("shipping_address", {})

    html = f"""
    <html>
    <head>
      <meta charset="UTF-8">
      <style>
        @font-face {{
            font-family: 'Cairo';
            src: url('fonts/Cairo-Regular.ttf') format('truetype');
            font-weight: normal;
        }}
        @font-face {{
            font-family: 'Cairo';
            src: url('fonts/Cairo-Bold.ttf') format('truetype');
            font-weight: bold;
        }}
        body {{
            font-family: 'Cairo', sans-serif;
        }}
      </style>
    </head>
    <body>
      <p style="text-align: right; margin: 0; font-size: 1.4em;">
        <strong>{order['name']}</strong>
      </p>
      <div style="margin: 1em 0;">
        <img src="https://i.ibb.co/dMZ03Zc/2d96914c-cac1-40a7-b8b8-bd3286ad39fa.png"
             alt="checkout-logo" style="max-height: 100px;" />
      </div>
      <hr />
      <h3>Item Details</h3>
      <table style="width: 100%; border-collapse: collapse; margin-bottom: 1.5em;">
        <thead>
          <tr style="background-color: #f5f5f5;">
            <th style="padding: 8px; border: 1px solid #ddd;">Product</th>
            <th style="padding: 8px; border: 1px solid #ddd;">Quantity</th>
            <th style="padding: 8px; border: 1px solid #ddd;">Item</th>
            <th style="padding: 8px; border: 1px solid #ddd;">Price</th>
          </tr>
        </thead>
        <tbody>
    """

    for li in order.get("line_items", []):
        qty   = li.get("quantity", 0)
        if qty <= 0: continue
        title = li.get("title", "")
        price = float(li.get("price", 0))
        img   = image_map.get(li.get("product_id"), "")

        html += f"""
        <tr>
          <td style="padding: 8px; border: 1px solid #ddd;">
            <img src="{img}" style="max-width: 60px;" />
          </td>
          <td style="padding: 8px; border: 1px solid #ddd; text-align: center;">
            <span style="font-size: 1.2em;"><strong>{qty}</strong></span>
          </td>
          <td style="padding: 8px; border: 1px solid #ddd; font-size: 1.1em;">
            <strong>{title}</strong>
            {"<br/><small>" + li.get("variant_title", "") + "</small>" if li.get("variant_title") else ""}
          </td>
          <td style="padding: 8px; border: 1px solid #ddd;">{price:.2f} EGP</td>
        </tr>
        """

    html += f"""
        </tbody>
      </table>
      <h3>Payment Summary</h3>
      <table style="width: 100%; border-collapse: collapse; margin-bottom: 1.5em;">
        <tr><td style="padding: 8px;">Subtotal:</td><td style="padding: 8px;">{true_subtotal:.2f} EGP</td></tr>
        <tr><td style="padding: 8px;">Discount:</td><td style="padding: 8px;">{total_discounts:.2f} EGP</td></tr>
        <tr><td style="padding: 8px;">Shipping:</td><td style="padding: 8px;">{shipping_price:.2f} EGP</td></tr>
        <tr><td style="padding: 8px;"><strong>Total:</strong></td><td style="padding: 8px;"><strong>{total_price:.2f} EGP</strong></td></tr>
    """

    if paid_amount > 0:
        html += f"""
        <tr>
          <td style="padding:8px;"><strong>Paid amount:</strong></td>
          <td style="padding:8px;"><strong>{paid_amount:.2f} EGP</strong></td>
        </tr>"""
    if outstanding > 0:
        html += f"""
        <tr>
          <td style="padding:8px;"><strong>Outstanding:</strong></td>
          <td style="padding:8px;"><strong>{outstanding:.2f} EGP</strong></td>
        </tr>"""
    html += "</table>"

    if note:
        html += f"""
      <h3>Note</h3>
      <div style="font-size:1.1em;">{note}</div>"""

    if ship_addr:
        html += f"""
      <h3>Shipping Details</h3>
      <div style="border:1px solid #000; padding:1em; font-size:1.1em; margin-bottom:1em; line-height:1.8;">
        <strong>{ship_addr.get('name')}</strong><br/>
        {ship_addr.get('address1')}<br/>
        {ship_addr.get('city')} {ship_addr.get('province_code')} {ship_addr.get('zip') or ''}<br/>
        {ship_addr.get('phone')}<br/>
        {ship_addr.get('country')}
      </div>"""

    html += """
      <p style="margin-top:2em;">
        For questions, contact us via WhatsApp <u><strong>+20 120 123 8905</strong></u><br/>
        Instagram: <strong>Koreanbeautysonlineshop</strong>
      </p>
    </body></html>
    """

    html_file = f"{order['name']}.html"
    pdf_file  = f"{order['name']}.pdf"
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html)
    HTML(html_file, base_url=".").write_pdf(pdf_file)

    tg_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendDocument"
    with open(pdf_file, "rb") as f:
        requests.post(tg_url, data={
            "chat_id": OTHER_CHAT_ID,
            "caption": f"📄 Invoice for {order['name']}"
        }, files={"document": (pdf_file, f, "application/pdf")})

    os.remove(html_file)
    os.remove(pdf_file)





seen_trackings = TTLCache(maxsize=100, ttl=6000)

@app.post("/tracking")
async def save_and_send_tracking(request: Request):
    data = await request.json()

    tracking   = data.get("tracking_number", "")
    order_name = data.get("name", "").replace(".1", "")



    seen_trackings[tracking] = True

    res = requests.post(
        BOSTA_URL,
        json={"trackingNumbers": tracking, "requestedAwbType": "A6", "lang": "en"},
        headers={"Authorization": BOSTA_TOKEN}
    )
    res.raise_for_status()
    awb_b64 = res.json().get("data", "")
    if awb_b64:
        awb_pdf = base64.b64decode(awb_b64)
        tg_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendDocument"
        requests.post(tg_url, data={
            "chat_id": OTHER_CHAT_ID,
            "caption": f"📄 AirwayBill for {order_name}"
        }, files={"document": (f"{order_name}ب.pdf", awb_pdf, "application/pdf")})

    order_id = data.get("order_id")
    shop_url = f"https://{SHOP_NAME}.myshopify.com/admin/api/{API_VERSION}/orders/{order_id}.json"
    shop_resp = requests.get(
        shop_url,
        headers={"X-Shopify-Access-Token": ACCESS_TOKEN}
    )
    shop_resp.raise_for_status()
    order = shop_resp.json().get("order", {})

    image_map = fetch_product_images(order.get("line_items", []))
    send_invoice_to_telegram(order, image_map)

    return {"status": "awb_sent_and_invoice_sent"}
