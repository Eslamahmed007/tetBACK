import logging
import sys
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
root_logger.handlers = [handler]

noisy_libs = ["fontTools", "weasyprint", "PIL"]
for lib in noisy_libs:
    logging.getLogger(lib).setLevel(logging.WARNING)

from fastapi import FastAPI, Request , Query
import base64
import datetime
from fastapi.responses import FileResponse
import os, requests
from weasyprint import HTML , CSS
from cachetools import TTLCache
import time


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

BOSTA_TOKEN = os.getenv("BOSTA_TOKEN")
BOSTA_URL = os.getenv("BOSTA_URL")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OTHER_CHAT_ID = os.getenv("OTHER_CHAT_ID")

SHOP_NAME     = os.getenv("SHOP_NAME")
API_VERSION   = os.getenv("API_VERSION")
ACCESS_TOKEN  = os.getenv("ACCESS_TOKEN")

def send_telegram(token, chat_id, message):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message}
    requests.post(url, data=payload)


def cancell(order):
    order_number = order.get("order_number")
    addr = order.get("shipping_address") or {}
    phone = addr.get("zip", "")
    phone1 = order.get("shipping_address", {}).get("phone", "").replace("+2", "").replace(" ", "")
    name = order.get("shipping_address", {}).get("name", "")
    msg=f"""📞 Whatsapp number = {phone}
📱 Phone number = {phone1}

Hi {name}

안녕하세요! to Korean Beautys 🌸

بنتواصل مع حضرتك لتأكيد انه قد تم إلغاء طلبك رقم 007{order_number}"""
    return msg



def formatt_order_messag(order):
    order_number = order.get("order_number")
    total_price = order.get("total_outstanding") + " EGP"
    addr = order.get("shipping_address") or {}
    phone = addr.get("zip", "")
    phone1 = order.get("shipping_address", {}).get("phone", "").replace("+2", "").replace(" ", "")
    address1 = order.get("shipping_address", {}).get("address1", "")
    name = order.get("shipping_address", {}).get("name", "")

    line_items = order.get("line_items", [])
    products = ""
    for item in line_items:
        if item['title'] =="Cash on Delivery fee" or item['title'] =='Normal Package' or item['title'] =='Premium Package':
            continue
        elif (item['current_quantity']==0):
            continue
        else:
            products += f"- {item['title']} (x{item['current_quantity']})\n"

    

    

    msg1 = f"""📞 Whatsapp number = {phone}
📱 Phone number = {phone1}

Hi {name} Korean Beautys with you

⏳ لو معندناش رد خلال 24 ساعة، الطلب بيتم إلغاءه تلقائيًا

بنتواصل مع حضرتك لتأكيد طلبك رقم 007{order_number} والدفع عن طريق instapay
{total_price}


📍 العنوان:
{address1}

🛍 محتويات الطلب:
{products}

📦 الطلب هيتم شحنه غدًا وهيوصل خلال 2–5 أيام من يوم التأكيد.

⸻

💳 طرق الدفع (InstaPay):
1️⃣ InstaPay – تحويل لحساب بنكي:
رقم الحساب: 01066350652

📸 بعد الدفع، برجاء إرسال صورة الإيصال علشان نبدأ إجراءات الشحن فورًا 💨
⸻

• في حالة الإلغاء بعد الشحن، بيتم تحصيل مصاريف الشحن (85 جنيه) من حضرتك.
• في حال كان العنوان غير واضح، يُرجى تحديده بدقة بذكر:
(المحافظة – المنطقة – أقرب معلم واضح) لتجنب أي تأخير في التوصيل.

شكراً لتفهمك واهتمامك بمنتجات Korean Beautys 💖
لو في أي استفسار، احنا دايمًا موجودين لخدمتك!"""

    
    return msg1


def messs(order):
    order_number = order.get("order_number")

    addr = order.get("shipping_address") or {}
    phone = addr.get("zip", "")
    phone1 = order.get("shipping_address", {}).get("phone", "").replace("+2", "").replace(" ", "")
    address1 = order.get("shipping_address", {}).get("address1", "")

    msg = f""" order number 007{order_number} has been paid
📞 Whatsapp number = {phone}
📱 Phone number = {phone1}
"""
    return msg


def format_order_messag(order):
    order_number = order.get("order_number")
    total_price = order.get("total_outstanding") + " EGP"

    addr = order.get("shipping_address") or {}
    phone = addr.get("zip", "")
    phone1 = order.get("shipping_address", {}).get("phone", "").replace("+2", "").replace(" ", "")
    address1 = order.get("shipping_address", {}).get("address1", "")
    name = order.get("shipping_address", {}).get("name", "")

    line_items = order.get("line_items", [])
    products = ""
    for item in line_items:
        if item['title'] =="Cash on Delivery fee" or item['title'] =='Normal Package' or item['title'] =='Premium Package':
            continue
        elif (item['current_quantity']==0):
            continue
        else:
            products += f"- {item['title']} (x{item['current_quantity']})\n"

    

    

    msg = f"""📞 Whatsapp number = {phone}
📱 Phone number = {phone1}

Hi {name} Korean Beautys with you

⏳ لو معندناش رد خلال 24 ساعة، الطلب بيتم إلغاءه تلقائيًا.

بنتواصل مع حضرتك لتأكيد طلبك رقم 007{order_number}
بمبلغ {total_price} 

📍 العنوان:
{address1}

🛍 محتويات الطلب:
{products}

📦 الطلب هيتم شحنه غدًا وهيوصل خلال 2–5 أيام من يوم التأكيد.

• في حالة الإلغاء بعد الشحن، بيتم تحصيل *مصاريف الشحن (85 جنيه)* من حضرتك.

• في حال كان العنوان غير واضح، يُرجى تحديده بدقة بذكر:  
(المحافظة – المنطقة – أقرب معلم واضح) لتجنب أي تأخير في التوصيل.  


شكراً لتفهمك واهتمامك بمنتجات Korean Beautys 💖
لو في أي استفسار، احنا موجودين دايمًا لخدمتك."""

    
    return msg

@app.post("/webhook")
async def handle_order(request: Request):
    data = await request.json()
    paid = data.get("financial_status", "")
    if paid=="Paid" or paid=="paid":

        return {"status": "paid - skipped"}
    
    elif "Instapay" in data.get("payment_gateway_names", []):
        message = formatt_order_messag(data)
        send_telegram(PRE_BOT_TOKEN, PRE_CHAT_ID, message)
        return {"status": "sent to prepaid bot"}
    

    else:
        message = format_order_messag(data)
        send_telegram(OTHER_BOT_TOKEN, OTHER_CHAT_ID, message)

        return {"status": "sent"}

seen_edit = TTLCache(maxsize=100, ttl=6000)

@app.post("/edit")
async def edit_order(request: Request):
    data1 = await request.json() 
    order_id = data1.get("order_edit").get("order_id")
    if order_id in seen_edit:
        return {"status": "duplicate_tracking_skipped"}

    seen_edit[order_id] = True
    
    shop_url = f"https://{SHOP_NAME}.myshopify.com/admin/api/{API_VERSION}/orders/{order_id}.json"
    shop_resp = requests.get(
        shop_url,
        headers={"X-Shopify-Access-Token": ACCESS_TOKEN}
    )
    shop_resp.raise_for_status()
    data = shop_resp.json().get("order", {})
    paid = data.get("financial_status", "")
    if paid=="Paid" or paid=="paid":

        return {"status": "paid - skipped"}
    
    elif "Instapay" in data.get("payment_gateway_names", []):
        message = formatt_order_messag(data)
        send_telegram(PRE_BOT_TOKEN, PRE_CHAT_ID, message)
        return {"status": "sent to prepaid bot"}
    

    else:
        message = format_order_messag(data)
        send_telegram(OTHER_BOT_TOKEN, OTHER_CHAT_ID, message)

        return {"status": "sent"}



seen_ord = TTLCache(maxsize=100, ttl=6000)

@app.post("/cancel")
async def cancel_order(request: Request):
    data = await request.json()
    order_id = data.get("order_id")
    if order_id in seen_ord:
        return {"status": "duplicate_tracking_skipped"}

    seen_ord[order_id] = True
    paid = data.get("financial_status", "")
    
    if paid=="Paid" or paid=="paid":

        return {"status": "paid - skipped"}
    
    elif "Instapay" in data.get("payment_gateway_names", []):
        message = cancell(data)
        send_telegram(PRE_BOT_TOKEN, PRE_CHAT_ID, message)
        return {"status": "sent to prepaid bot"}
    

    else:
        message = cancell(data)
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




def fetch_product_images(line_items):
    image_map = {}
    for li in line_items:
        pid = li.get("product_id")
        if pid and pid not in image_map:
            try:
                url = f"https://{SHOP_NAME}.myshopify.com/admin/api/{API_VERSION}/products/{pid}.json?fields=image"
                r = requests.get(url, headers={"X-Shopify-Access-Token": ACCESS_TOKEN})
                r.raise_for_status()
                img_url = r.json().get("product", {}).get("image", {}).get("src", "")

                if img_url and requests.head(img_url, timeout=3).status_code == 200:
                    image_map[pid] = img_url
                else:
                    image_map[pid] = ""
            except Exception as e:
                logging.warning(f"Failed to load product image {pid}: {e}")
                image_map[pid] = ""
    return image_map

def send_invoice_to_telegram(order: dict, image_map: dict):
    try:
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
                margin: 0;
                padding: 0;
                font-size: 12px;
                line-height: 1.4;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-bottom: 0.8em;
            }}
            th, td {{
                padding: 4px;
                border: 1px solid #ddd;
            }}
            h3 {{
                margin: 0.6em 0 0.4em;
            }}
            p {{
                margin: 0.4em 0;
            }}
            strong {{
                font-weight: bold;
            }}
        </style>
        </head>
        <body>
        <p style="text-align: right; margin: 0; font-size: 1.3em;"><strong>{order['name']}</strong></p>
        <div style="margin: 0.5em 0;">
            <img src="https://i.ibb.co/dMZ03Zc/2d96914c-cac1-40a7-b8b8-bd3286ad39fa.png"
                alt="checkout-logo" style="max-height: 80px;" />
        </div>
        <hr />
        <h3>Item Details</h3>
        <table>
            <thead>
            <tr style="background-color: #f5f5f5;">
                <th>Product</th>
                <th>Quantity</th>
                <th>Item</th>
                <th>Price</th>
            </tr>
            </thead>
            <tbody>
        """

        for li in order.get("line_items", []):
            qty   = li.get("current_quantity", 0)
            if qty <= 0: continue
            title = li.get("title", "")
            price = float(li.get("price", 0))
            img   = image_map.get(li.get("product_id"), "")

            html += f"""
            <tr>
            <td><img src="{img}" style="max-width: 50px;" /></td>
            <td style="text-align: center;"><strong>{qty}</strong></td>
            <td>
                <strong>{title}</strong>
                {"<br/><small>" + li.get("variant_title", "") + "</small>" if li.get("variant_title") else ""}
            </td>
            <td>{price:.2f} EGP</td>
            </tr>
            """
        if shipping_lines:
            shipping_line = shipping_lines[0]
            shipping_title = shipping_line.get("title", "Shipping")
            raw_price = float(shipping_line.get("price", 0))
            discounted_price = float(shipping_line.get("discounted_price", raw_price))

            if discounted_price < raw_price:
                price_display = f"<del>{raw_price:.2f} EGP</del><br/><strong>{discounted_price:.2f} EGP</strong>"
            else:
                price_display = f"{raw_price:.2f} EGP"

            html += f"""
            <tr style="background-color: #f9f9f9;">
                <td colspan="2" style="font-weight: bold;">Shipping Method</td>
                <td style="font-weight: bold;">{shipping_title}</td>
                <td>{price_display}</td>
            </tr>
            """

        html += f"""
            </tbody>
        </table>
        <h3>Payment Summary</h3>
        <table>
            <tr><td>Subtotal:</td><td>{true_subtotal:.2f} EGP</td></tr>
            <tr><td>Discount:</td><td>{total_discounts:.2f} EGP</td></tr>
            <tr><td>Shipping:</td><td>{shipping_price:.2f} EGP</td></tr>
            <tr><td><strong>Total:</strong></td><td><strong>{total_price:.2f} EGP</strong></td></tr>
        """

        if paid_amount > 0:
            html += f"""
            <tr><td><strong>Paid amount:</strong></td><td><strong>{paid_amount:.2f} EGP</strong></td></tr>"""

        if outstanding > 0:
            html += f"""
            <tr><td><strong>Outstanding:</strong></td><td><strong>{outstanding:.2f} EGP</strong></td></tr>"""

        html += "</table>"

        if note:
            html += f"""
        <h3>Note</h3>
        <div style="font-size:1.1em;">{note}</div>"""

        if ship_addr:
            html += f"""
        <h3>Shipping Details</h3>
        <div style="border:1px solid #000; padding:0.6em; font-size:1.1em; margin-bottom:0.8em; line-height:1.4;">
            <strong>{ship_addr.get('name')}</strong><br/>
            {ship_addr.get('address1')}<br/>
            {ship_addr.get('city')} {ship_addr.get('province_code')} {ship_addr.get('zip') or ''}<br/>
            {ship_addr.get('phone')}<br/>
            {ship_addr.get('country')}
        </div>"""

        html += """
        <p style="margin-top: 1.2em;">
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
    except Exception as e:
        logging.error(f"Failed to send invoice: {e}")





seen_trackings = TTLCache(maxsize=100, ttl=6000)

@app.post("/tracking")
async def save_and_send_tracking(request: Request):
    try:
        data = await request.json()
        tracking = data.get("tracking_number", "")
        order_name = data.get("name", "").replace(".1", "")
        if tracking in seen_trackings:
            return {"status": "duplicate_tracking_skipped"}

        seen_trackings[tracking] = True

        attempts = 3
        for i in range(attempts):
            try:
                res = requests.post(
                    BOSTA_URL,
                    json={"trackingNumbers": tracking, "requestedAwbType": "A6", "lang": "en"},
                    headers={"Authorization": BOSTA_TOKEN},
                    timeout=5
                )
                res.raise_for_status()
                break
            except requests.exceptions.ReadTimeout:
                logging.warning(f"Timeout from Bosta - attempt {i+1}")
                time.sleep(1)
        else:
            raise Exception("AWB request failed after several attempts")

        awb_b64 = res.json().get("data", "")
        if awb_b64:
            awb_pdf = base64.b64decode(awb_b64)
            tg_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendDocument"
            requests.post(tg_url, data={
                "chat_id": OTHER_CHAT_ID,
                "caption": f"📄 AirwayBill for {order_name}"
            }, files={"document": (f"ب {order_name}.pdf", awb_pdf, "application/pdf")})

        order_id = data.get("order_id")
        shop_url = f"https://{SHOP_NAME}.myshopify.com/admin/api/{API_VERSION}/orders/{order_id}.json"
        shop_resp = requests.get(shop_url, headers={"X-Shopify-Access-Token": ACCESS_TOKEN})
        shop_resp.raise_for_status()
        order = shop_resp.json().get("order", {})
        image_map = fetch_product_images(order.get("line_items", []))
        send_invoice_to_telegram(order, image_map)

        return {"status": "awb_sent_and_invoice_sent"}

    except Exception as e:
        logging.error(f"Error during /tracking execution: {e}")
        return {"status": "error", "message": str(e)}
    

seen_paid = TTLCache(maxsize=100, ttl=6000)

@app.post("/payment")
async def handle_payment(request: Request):
    try:
        data = await request.json()
        order_id = data.get("order_id")
        if order_id in seen_paid:
            return {"status": "duplicate_tracking_skipped"}

        seen_paid[order_id] = True
        gateways = data.get("payment_gateway_names", [])
        message = messs(data)

        if "Cash on Delivery (COD)" in gateways:
            province = (
                data.get("shipping_address", {}).get("province_code", "") or
                data.get("billing_address", {}).get("province_code", "")
            ).lower()
            non=data.get("shipping_address", {}).get("city", "")

            send_telegram(OTHER_BOT_TOKEN, OTHER_CHAT_ID, message)

        elif "Instapay" in gateways:
            send_telegram(PRE_BOT_TOKEN, PRE_CHAT_ID, message)
            return {"status": "sent to instapay bot"}


        return {"status": "success"}

    except Exception as e:
        logging.error(f"Error in /payment: {e}")
        return {"status": "error", "message": str(e)}
