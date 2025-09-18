

import streamlit as st
from dotenv import load_dotenv
import os
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain_openai import ChatOpenAI

# .envの読み込み（APIキーなどの管理用）
load_dotenv()

def show_app_header():
    st.title("専門家アドバイスアプリ：ビジネスコンサルタント × 心理カウンセラー")
    st.markdown("""
**このアプリについて**  
ビジネス課題やメンタル面の悩みについて、AIが専門家になりきって100文字以内でアドバイスを返します。

**操作方法**  
1. 上部のラジオボタンで「ビジネスコンサルタント」または「心理カウンセラー」を選択してください。
2. 相談したい内容や質問を入力欄に記入してください。
3. 「実行」ボタンを押すと、AIが専門家としてアドバイスを返します。

---
""")
    st.write("##### 動作モード1: ビジネスコンサルタント")
    st.write("ビジネス課題の解決や戦略アドバイスをする専門家としてAIが回答します。")
    st.write("##### 動作モード2: 心理カウンセラー")
    st.write("メンタル面や人間関係に配慮してアドバイスする専門家としてAIが回答します。")

def select_mode():
    return st.radio(
        "動作モードを選択してください。",
        ["ビジネスコンサルタント", "心理カウンセラー"]
    )

def get_user_question():
    return st.text_input(label="相談内容や質問を入力してください。")

def build_prompt(genre: str, question: str):
    """ジャンルと質問からプロンプトを生成（タプル記法で簡素化）"""
    system_message = f"あなたは、{genre}として振る舞うAIです。ユーザーからの質問に100文字以内で回答してください。"
    human_message = question
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_message),
        ("human", human_message),
    ])
    return prompt.format_prompt().to_messages()


def get_expert_advice(user_question: str, selected_item: str) -> str:
    """
    入力テキスト（user_question）とラジオボタンの選択値（selected_item）を受け取り、
    LLMからの回答を返す。
    """
    genre = selected_item
    messages = build_prompt(genre, user_question)
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    result = llm.invoke(messages)
    return result.content


def main():
    # APIキーの存在チェック（OpenAI APIキー例: OPENAI_API_KEY）
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        st.error(".envファイルにOpenAIのAPIキー(OPENAI_API_KEY)が設定されていません。設定後、再度アプリを起動してください。")
        return

    show_app_header()
    selected_item = select_mode()
    st.divider()
    user_question = get_user_question()

    if st.button("実行"):
        st.divider()
        if not user_question:
            st.error("相談内容や質問を入力してから「実行」ボタンを押してください。")
            return
        try:
            advice = get_expert_advice(user_question, selected_item)
            st.write(advice)
        except Exception as e:
            st.error(f"AIからの回答取得時にエラーが発生しました: {e}")

if __name__ == "__main__":
    main()