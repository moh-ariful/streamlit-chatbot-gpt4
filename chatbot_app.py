import streamlit as st
import openai

# Mengatur API key
openai.api_key = 'sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'  # Ganti dgn API key yg benar

st.title('Chatbot dengan GPT-4 Turbo')

# Slider utk menentukan nilai temperature dgn keterangan
temperature = st.slider(
    'Atur tingkat kreativitas chatbot (0 = Lebih Deterministik, 1 = Sangat Kreatif):',
    min_value=0.0, max_value=1.0, value=0.5, step=0.01,
    format="%.2f"  # Menampilkan dua angka desimal
)

# Area untuk input pengguna
user_input = st.text_input("Masukkan pesan di sini:", key="user_input")

# Inisialisasi state sesi utk history jika belum ada
if 'history' not in st.session_state:
    st.session_state['history'] = []

# Fungsi utk menambahkan pesan user & bot ke dalam history
def append_to_history(role, content):
    st.session_state['history'].append({"role": role, "content": content})

# Fungsi utk mendapatkan respons chatbot dga peran tertentu & temperature tertentu
def get_chatbot_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-1106-preview",
            messages=st.session_state['history'] + [
                # Pesan untuk chatbot untuk berperan sebagai Pengembang Python dan Pemburu Bug Bounty
                {"role": "system", "content": "Anda adalah Pengembang Python yang terampil dan Pemburu Bug Bounty. Anda memandu pengguna dengan petunjuk, trik, dan teknik yang relevan dengan pengembangan Python dan pemburuan bug."},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature  # Menggunakan nilai temperature dari slider
        )
        return response.choices[0].message['content']
    except Exception as e:
        # Menampilkan error jika terjadi kesalahan
        st.error("Maaf, terjadi kesalahan: " + str(e))
        return None

# Fungsi utk menampilkan respons chatbot dalam area yg lebih besar
def display_chatbot_response(bot_response):
    st.text_area("Respon Chatbot", value=bot_response, height=300, max_chars=None)

# Menangani input pengguna
if user_input:
    # Menambahkan input pengguna ke dalam history
    append_to_history("user", user_input)
    # Mendapatkan respons dari chatbot
    bot_response = get_chatbot_response(user_input)
    if bot_response:
        # Menambahkan respons chatbot ke dalam history
        append_to_history("assistant", bot_response)
        # Menampilkan respons chatbot
        display_chatbot_response(bot_response)
