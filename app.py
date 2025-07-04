import requests
from fastapi import FastAPI, Request

app = FastAPI()

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

    line_items = order.get("line_items", [])
    products = ""
    for item in line_items:
        products += f"- {item['title']} (x{item['quantity']})\n"

    msg = f"""Whatsapp number ={phone}
phone number= {phone1}

안녕하세요!  to Korean Beautys   🌸  

بنتواصل مع حضرتك لتأكيد طلبك رقم 007{order_number}

بمبلغ {total_price}

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
    message = format_order_message(data)
    paid = data.get("financial_status", "")
    codes = data.get("discount_codes", [])
    code_values = [c.get("code", "") for c in codes]
    codes_text = ", ".join(filter(None, code_values)) or "NO"
    if "PREPAID" in codes_text:
        send_telegram(PRE_BOT_TOKEN, PRE_CHAT_ID, message)
        return {"status": "sent to prepaid bot"}
    
    elif paid=="Paid" or paid=="paid":

        return {"status": "prepaid - skipped"}
    

    else:


        province = (
            data.get("shipping_address", {}).get("province_code", "") or
            data.get("billing_address", {}).get("province_code", "")
        ).lower()


        if "alx" in province:
            send_telegram(ALEX_BOT_TOKEN, ALEX_CHAT_ID, message)
        else:
            send_telegram(OTHER_BOT_TOKEN, OTHER_CHAT_ID, message)

        return {"status": "sent"}
