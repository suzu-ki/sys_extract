import streamlit as st
import os
from main_spacy import app
from io import BytesIO

def process_pdf(file):
    # PDFの解析処理をここに実装
    file_data = file.read()
    pdf = BytesIO(file_data)
    setlist, keylist = app(pdf)
    
    return list(setlist), list(keylist)

st.title("専門用語抽出ツール")

# PDFアップロード
pdf_file = st.file_uploader("PDFをアップロード", type=["pdf"])

if pdf_file is not None:
    terms, key = process_pdf(pdf_file)
    
    st.subheader("数字入力欄:")
    # 数字の選択を動的に表示
    col1n, col2n = st.columns(2)
    with col1n:
        # keyのインデックスを選択
        number_input2 = st.number_input("数字を選択 (key)", min_value=0, max_value=len(key)-1, step=1, key="f2")

    with col2n:
        # termsのインデックスを選択
        number_input1 = st.number_input("数字を選択 (terms)", min_value=0, max_value=len(terms)-1, step=1, key="f1")

    # 変更後に表示される内容を確認
    st.write("以下の文字列をコピーし、Consensusに入力してください:")
    st.write("Please explain " + str(terms[number_input1]) + " related " + str(key[number_input2]))
    st.write("https://consensus.app/")
        
        
    st.subheader("抽出結果")
    
    # Streamlitの列を作成
    col1, col2 = st.columns(2)

    with col1:
        st.write("抽出されたkeywords:")
        
        # キーワード検索用のテキスト入力
        filter_key = st.text_input("検索", key="filter_key_input")
        
        # filter_key が入力された場合、keyリストをフィルタリング
        if filter_key:
            filtered_key = [(index, term) for index, term in enumerate(key) if filter_key.lower() in term.lower()]
        else:
            filtered_key = [(index, term) for index, term in enumerate(key)]  # フィルタリングなしの場合

        # フィルタリング後のキーワードリストを表示
        st.write("keywordリスト:")
        for index, term in filtered_key:
            st.write(f"番号: {index} - {term}")
        
    with col2:
        st.write("抽出された専門用語:")
        
        # 専門用語検索用のテキスト入力
        filter_term = st.text_input("検索", key="filter_term_input")
        
        # filter_term が入力された場合、termsリストをフィルタリング
        if filter_term:
            filtered_terms = [(index, term) for index, term in enumerate(terms) if filter_term.lower() in term.lower()]
        else:
            filtered_terms = [(index, term) for index, term in enumerate(terms)]  # フィルタリングなしの場合

        # フィルタリング後の専門用語リストを表示
        st.write("専門用語リスト:")
        for index, term in filtered_terms:
            st.write(f"番号: {index} - {term}")


