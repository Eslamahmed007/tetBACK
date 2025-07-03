import requests
from fastapi import FastAPI, Request

app = FastAPI()

# توكنات البوتات
ALEX_BOT_TOKEN = "7569464405:AAHosRAyvKcherRu_iMcgapopnqsmmOLmEU"
ALEX_CHAT_ID = "1110037703"

OTHER_BOT_TOKEN = "2147453430:AAFc3aKabHmjfJP_ubW2jjfHkxoq1zj3GnM"
OTHER_CHAT_ID = "1110037703"

def send_telegram(token, chat_id, message):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message}
    requests.post(url, data=payload)

def format_order_message(order):
    order_number = order.get("order_number")
    total_price = order.get("total_price") + " EGP"
    phone = order.get("shipping_address", {}).get("phone", "").replace("+", "").replace(" ", "")
    
    line_items = order.get("line_items", [])
    products = ""
    for item in line_items:
        products += f"- {item['title']} (x{item['quantity']})\n"

    msg = f"""wa.me/{phone}

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

    province = (
        data.get("shipping_address", {}).get("province", "") or
        data.get("billing_address", {}).get("province", "")
    ).lower()

    message = format_order_message(data)

    if "alexandria" in province:
        send_telegram(ALEX_BOT_TOKEN, ALEX_CHAT_ID, message)
    else:
        send_telegram(OTHER_BOT_TOKEN, OTHER_CHAT_ID, message)

    return {"status": "sent"}
