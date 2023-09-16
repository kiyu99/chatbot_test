
import streamlit as st
import openai

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

system_prompt = """
あなたは優秀で聞き上手な学びのアウトプットコーチです。
生徒のやる気を引き出しアウトプットの質を高める方向に会話をリードし、生徒の学びのアウトプットを手助けしてください。生徒のレベルに合わせて適切なアドバイスも行ってください。
会話は自然な流れで、あなたは「今日は何を学びましたか？」から会話をスタートさせます。一度に3つ以上質問しないでください。生徒の返事に対し興味をもってリアクションや会話を膨らましてください。
会話が5往復ほどしたら、それまでの内容を要約してください。
あなたの役割は生徒の学びのアウトプットを聞き出すことなので、あなたの発言が長くなりすぎないようにしてください。
"""

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": system_prompt}
        ]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去


# ユーザーインターフェイスの構築
st.title("My AI Assistant")
st.write("ChatGPT APIを使ったチャットボットです。")

# メッセージ表示エリア
if st.session_state["messages"]:
    messages = st.session_state["messages"]
    for message in messages:
        speaker = "🙂" if message["role"] == "user" else "🤖"
        st.write(speaker + ": " + message["content"])

# メッセージ入力ボックス
user_input = st.text_input("メッセージを入力してください。", key="user_input", on_change=communicate)
