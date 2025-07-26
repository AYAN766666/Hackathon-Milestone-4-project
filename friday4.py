
import streamlit as st
import hashlib
import base64
from cryptography.fernet import Fernet

# Streamlit پیج سیٹنگ
st.set_page_config(page_title="🔐 محفوظ ڈیٹا", page_icon="🔐", layout="centered")

# ==== Fernet key بنانے والا فنکشن ====
def generate_key(passkey: str) -> bytes:
    hashed = hashlib.sha256(passkey.encode()).digest()
    return base64.urlsafe_b64encode(hashed)

# ==== Encryption فنکشن ====
def encrypt(text: str, passkey: str) -> str:
    key = generate_key(passkey)
    f = Fernet(key)
    encrypted = f.encrypt(text.encode())
    return encrypted.decode()

# ==== Decryption فنکشن ====
def decrypt(encrypted_text: str, passkey: str) -> str | None:
    try:
        key = generate_key(passkey)
        f = Fernet(key)
        decrypted = f.decrypt(encrypted_text.encode())
        return decrypted.decode()
    except:
        return None

# ==== سیشن ویری ایبلز ====
if "failed_attempts" not in st.session_state:
    st.session_state.failed_attempts = 0

if "logged_in" not in st.session_state:
    st.session_state.logged_in = True

# ==== سائیڈبار مینو ====
menu = st.sidebar.radio("📋 مینو منتخب کریں:", ["🏠 ہوم", "🔐 انکرپٹ کریں", "🔓 ڈی کرپٹ کریں", "🔑 لاگ ان"])

# ==== ہوم پیج ====
if menu == "🏠 ہوم":
    st.title("🔐 محفوظ انکرپشن ایپ")
    st.markdown("یہ ایپ آپ کے ڈیٹا کو پاسکی کے ذریعے انکرپٹ اور ڈی کرپٹ کرتی ہے۔")

# ==== انکرپشن پیج ====
elif menu == "🔐 انکرپٹ کریں":
    st.header("🔐 ڈیٹا انکرپٹ کریں")
    text = st.text_area("✍️ اپنا ڈیٹا لکھیں:")
    passkey = st.text_input("🔑 پاسکی:", type="password")

    if st.button("انکرپٹ کریں"):
        if text and passkey:
            encrypted = encrypt(text, passkey)
            st.success("✅ ڈیٹا انکرپٹ ہو گیا!")
            st.code(encrypted)
        else:
            st.warning("⚠️ براہ کرم تمام فیلڈز پر کریں۔")

# ==== ڈی کرپشن پیج ====
elif menu == "🔓 ڈی کرپٹ کریں":
    if not st.session_state.logged_in:
        st.warning("🔒 آپ لاگ آؤٹ ہیں، براہ کرم لاگ ان کریں۔")
    else:
        st.header("🔓 ڈیٹا ڈی کرپٹ کریں")
        encrypted_text = st.text_area("🔐 انکرپٹ شدہ ڈیٹا:")
        passkey = st.text_input("🔑 پاسکی:", type="password")

        if st.button("ڈی کرپٹ کریں"):
            if encrypted_text and passkey:
                result = decrypt(encrypted_text, passkey)
                if result:
                    st.success("✅ ڈیٹا کامیابی سے ڈی کرپٹ ہو گیا!")
                    st.code(result)
                    st.session_state.failed_attempts = 0
                else:
                    st.session_state.failed_attempts += 1
                    attempts_left = 3 - st.session_state.failed_attempts
                    st.error(f"❌ پاسکی غلط ہے! باقی کوششیں: {attempts_left}")
                    if attempts_left <= 0:
                        st.session_state.logged_in = False
                        st.warning("🚫 آپ لاگ آؤٹ ہو چکے ہیں۔")

# ==== لاگ ان پیج ====
elif menu == "🔑 لاگ ان":
    st.header("🔑 لاگ ان کریں")
    master_password = st.text_input("پاسورڈ:", type="password")

    if st.button("لاگ ان"):
        if master_password == "admin123":
            st.session_state.logged_in = True
            st.session_state.failed_attempts = 0
            st.success("✅ لاگ ان کامیاب!")
        else:
            st.error("❌ غلط پاسورڈ!")

# ==== سائیڈ معلومات ====
with st.sidebar.expander("ℹ️ معلومات"):
    st.write("یہ ایپ RAM میں عارضی طور پر ڈیٹا رکھتی ہے۔")
    st.write("Fernet انکرپشن استعمال کی گئی ہے۔")
