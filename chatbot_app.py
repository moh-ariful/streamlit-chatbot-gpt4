import streamlit as st
import openai

# Mengatur API key
openai.api_key = 'sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'  # Ganti dgn API key yg benar

st.title('Chatbot dengan GPT-4 Turbo')

# Dropdown untuk memilih model
model_choice = st.selectbox(
    'Pilih Model Bahasa:',
    ('gpt-3.5-turbo', 'gpt-4-1106-preview'),
    index=1  # Index default ke GPT-4
)

# Slider untuk menentukan nilai temperature
temperature = st.slider(
    'Atur tingkat kreativitas chatbot (0 = Lebih Deterministik, 1 = Sangat Kreatif):',
    min_value=0.0, max_value=1.0, value=0.5, step=0.01,
    format="%.2f"  # Menampilkan dua angka desimal
)

# Area untuk input pengguna
user_input = st.text_input("Masukkan pesan di sini:", key="user_input")

# Inisialisasi state sesi untuk history jika belum ada
if 'history' not in st.session_state:
    st.session_state['history'] = []

# Fungsi untuk menambahkan pesan user & bot ke dalam history
def append_to_history(role, content):
    st.session_state['history'].append({"role": role, "content": content})

# Fungsi untuk mendapatkan respons chatbot dengan model tertentu
def get_chatbot_response(prompt, model):
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=st.session_state['history'] + [
                {"role": "system", "content": "Anda adalah Pengembang Python yang terampil dan Pemburu Bug Bounty. Anda memandu pengguna dengan petunjuk, trik, dan teknik yang relevan dengan pengembangan Python dan pemburuan bug."},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature
        )
        return response.choices[0].message['content']
    except Exception as e:
        st.error("Maaf, terjadi kesalahan: " + str(e))
        return None

# Fungsi untuk menampilkan respons chatbot
def display_chatbot_response(bot_response):
    st.text_area("Respon Chatbot", value=bot_response, height=300, max_chars=None)

# Menangani input pengguna
if user_input:
    append_to_history("user", user_input)
    bot_response = get_chatbot_response(user_input, model_choice)
    if bot_response:
        append_to_history("assistant", bot_response)
        display_chatbot_response(bot_response)
