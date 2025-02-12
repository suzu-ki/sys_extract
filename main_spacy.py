import spacy
from pdf_t1 import extract_body_text2, extract_body_text3
import re

nlp = spacy.load('en_core_web_sm')

# spaCyのモデルをロード
def tokenize_text(text):
    # テキストを解析
    doc = nlp(text)

    # # 名詞句を抽出
    # specialized_terms = set([chunk.text for chunk in doc.noun_chunks if not re.search(r'\d', chunk.text)])
    # print(specialized_terms)
    
    w_list = set()
    not_list = set()
    # 固有表現の抽出（論文内の重要な名前や理論など）
    for ent in doc.ents:
        lab = ent.label_
        te = ent.text
        if not lab in ['ORG', 'PRODUCT', 'WORK_OF_ART', 'MISC']:
            not_list.add(te)
        else:
            if not re.search(r'\d', te) or not 'University' in te:
                if not 'IEEE' in te:
                    # print(te)
                    w_list.add(te)
        # print(f"Entity: {ent.text}, Label: {ent.label_}")
    
    # result = (specialized_terms | w_list) - not_list

    # 名詞句のリスト
    # print(specialized_terms)
    # return result
    return w_list

def tokenize_text_title(text):
    # テキストを解析
    doc = nlp(text)

    # # 名詞句を抽出
    specialized_terms = set([chunk.text for chunk in doc.noun_chunks if not re.search(r'\d', chunk.text)])    
    
    w_list = set()
    not_list = set()
    # 固有表現の抽出（論文内の重要な名前や理論など）
    for ent in doc.ents:
        lab = ent.label_
        te = ent.text
        if not lab in ['ORG', 'PRODUCT', 'WORK_OF_ART', 'MISC']:
            not_list.add(te)
        else:
            if not re.search(r'\d', te) or not 'University' in te:
                w_list.add(te)
        # print(f"Entity: {ent.text}, Label: {ent.label_}")
    
    result = (specialized_terms | w_list) - not_list

    # 名詞句のリスト
    # print(specialized_terms)
    return result

def app(file):
    try:
        title_text, keytext, body_text = extract_body_text3(file)
    except FileNotFoundError:
        print("エラー: ファイルが見つかりませんでした。")
        title_text, keytext, body_text = "","",""
        
    words_english = tokenize_text(body_text)
    title_set = tokenize_text_title(title_text)
    setlist = words_english  | title_set
    # print(setlist)
    
    if keytext == '':
        print('keyword is not contain')
    else:
        keylist = keytext.split(', ')
        keylist[0] = keylist[0].split(': ')[1]
        # print("\nkeyリスト:")
        # print(keylist)
    
    return setlist, keylist


if __name__ == "__main__":
    dpath = './paper/'
    # filename = 'SiPhON提案論文.pdf'
    filename = 'sam2.pdf'
    try:
        title_text, keytext, body_text = extract_body_text2(dpath, filename)
    except FileNotFoundError:
        print("エラー: ファイルが見つかりませんでした。")
        title_text, keytext, body_text = "","",""
    # print("本文抽出結果:")
    # print(body_text)
    
    # word_list = tokenize_text(body_text)
    # print("抽出された単語リスト:")
    # print(word_list)
    
    words_english = tokenize_text(body_text)
    print("\n英語リスト:")
    # print(words_english)
    
    title_set = tokenize_text_title(title_text)
    # print(title_set)
    setlist = words_english  | title_set
    print(setlist)
    
    if keytext == '':
        print('keyword is not contain')
    else:
        keylist = keytext.split(', ')
        keylist[0] = keylist[0].split(': ')[1]
        print("\nkeyリスト:")
        print(keylist)
    
    
    # con = generate_compounds(words_kanji)
    # print(con)