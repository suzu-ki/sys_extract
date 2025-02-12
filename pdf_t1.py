from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTContainer, LTTextLine
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.high_level import extract_text
import re
from io import BytesIO

def get_objs(layout, results):
    """
    再帰的にPDFページ内のテキスト行を探索し、文章情報を取得する。
    """
    if not isinstance(layout, LTContainer):
        return
    for obj in layout:
        if isinstance(obj, LTTextLine):
            results.append({'text': obj.get_text().strip(), 'height': obj.height})
        get_objs(obj, results)

def fix_line_breaks(text):
    text = re.sub(r'([A-Za-z0-9])\n([A-Za-z0-9])', r'\1 \2', text)  # 英数字の間の改行を取り除く
    # text = re.sub(r'([^\x00-\x7F])\n([^\x00-\x7F])', r'\1\2', text)  # 日本語文字間の改行を取り除く
    return text

def extract_text_cleaned(text):
    cleaned_text = re.sub(r'\(cid:[0-9]+\)', '', text)
    # return cleaned_text
    return fix_line_breaks(cleaned_text)

def extract_body_text(dpath, filename):
    """
    PDFファイルから本文を抽出する関数。
    - dpath: PDFファイルのディレクトリパス
    - filename: ファイル名
    """
    pathname = dpath + filename
    f_references = True
    
    with open(pathname, "rb") as f:
        parser = PDFParser(f)
        document = PDFDocument(parser)
        laparams = LAParams(all_texts=True)
        rsrcmgr = PDFResourceManager()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        
        body_text = []
        keytext = ''
        flag1 = True
        flag2 = False
        # f_references = True
        for page in PDFPage.create_pages(document):
            interpreter.process_page(page)
            layout = device.get_result()
            results = []
            get_objs(layout, results)
            if flag1:
                max_height = max(results, key=lambda x: x['height'])['height']
                max_height_items = [item for item in results if item['height'] == max_height]
                title_text = ''
                for item in max_height_items:
                    title_text += (item.get('text').strip() + " ")
                print(title_text, max_height_items)
                flag1 = False
            
            # 各行のテキストをフィルタリングして本文を抽出
            for text_line in results:
                text = text_line.get('text')
                
                if ('keywords:' in text or 'Keywords:' in text) and not flag2:
                    keytext = text
                    flag2 = True
                    print(text)
                    continue
                
                # 空行や短い行、セクション番号などを除外
                
                # 参考文献セクションの開始を検出
                if f_references:
                    if re.search(r'\b(References|REFERENCES|Bibliography|Works Cited|Cited Works)\b', text):
                        f_references = False
                        print('!!!!!!!!!')
                        continue  # 参考文献開始後のテキストはスキップ
                
                if not f_references:
                    print('llll')
                    break
                
                
                if len(text) < 15 or re.match(r'^\d+(\.\d+)*$', text):
                    continue
                
                if flag2:
                    body_text.append(text)
    
    # return "\n".join(body_text)
    return extract_text_cleaned("\n".join(body_text))

def extract_body_text2(dpath, filename):
    """
    PDFファイルから本文を抽出する関数。
    - dpath: PDFファイルのディレクトリパス
    - filename: ファイル名
    """
    pathname = dpath + filename
    f_references = True  # 参考文献を含めるかのフラグ
    
    with open(pathname, "rb") as f:
        parser = PDFParser(f)
        document = PDFDocument(parser)
        laparams = LAParams(all_texts=True)
        rsrcmgr = PDFResourceManager()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        
        body_text = []
        keytext = ''
        flag1 = True
        flag2 = False

        for page in PDFPage.create_pages(document):
            interpreter.process_page(page)
            layout = device.get_result()
            results = []
            get_objs(layout, results)
            
            if flag1:
                max_height = max(results, key=lambda x: x['height'])['height']
                max_height_items = [item for item in results if item['height'] == max_height]
                title_text = ''
                for item in max_height_items:
                    title_text += (item.get('text').strip() + " ")
                # print(title_text.strip(), max_height_items)
                flag1 = False
            
            for text_line in results:
                text = text_line.get('text')
                # print(text)
                # continue

                # Keywordsの検出
                if ('keywords:' in text or 'Keywords:' in text) and not flag2:
                    keytext = text
                    flag2 = True
                    # print(text)
                    continue
                
                # 不要な短い行や番号のみの行を除外
                if len(text) < 15 or re.match(r'^\d+(\.\d+)*$', text):
                    # print(text)
                    # 参考文献セクションの開始を検出
                    if re.search(r'\b(References|REFERENCES|Bibliography|Works Cited|Cited Works)\b', text):
                        f_references = False  # 参考文献を無視するようにフラグを変更
                        print('Detected References Section, Stopping Text Collection.')
                        print(text)
                        return title_text, keytext, extract_text_cleaned("\n".join(body_text))  # ここで本文抽出を終了
                    continue

                # 本文のリストに追加
                if flag2:
                    # print(text)
                    body_text.append(text)
    
    print('end')
    return title_text, keytext, extract_text_cleaned("\n".join(body_text))



def extract_body_text3(file):
    # body_text = extract_text(file)
    # if not body_text:
    #     body_text = ""
    
    # print(body_text)
    # exit(0)
    
    f_references = True  # 参考文献を含めるかのフラグ
    
    parser = PDFParser(file)
    document = PDFDocument(parser)
    laparams = LAParams(all_texts=True)
    rsrcmgr = PDFResourceManager()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    
    body_text = []
    keytext = ''
    flag1 = True
    flag2 = False

    for page in PDFPage.create_pages(document):
        interpreter.process_page(page)
        layout = device.get_result()
        results = []
        get_objs(layout, results)
        
        if flag1:
            max_height = max(results, key=lambda x: x['height'])['height']
            max_height_items = [item for item in results if item['height'] == max_height]
            title_text = ''
            for item in max_height_items:
                title_text += (item.get('text').strip() + " ")
            # print(title_text.strip(), max_height_items)
            flag1 = False
        
        for text_line in results:
            text = text_line.get('text')
            # print(text)
            # continue

            # Keywordsの検出
            if ('keywords:' in text or 'Keywords:' in text) and not flag2:
                keytext = text
                flag2 = True
                # print(text)
                continue
            
            # 不要な短い行や番号のみの行を除外
            if len(text) < 15 or re.match(r'^\d+(\.\d+)*$', text):
                # print(text)
                # 参考文献セクションの開始を検出
                if re.search(r'\b(References|REFERENCES|Bibliography|Works Cited|Cited Works)\b', text):
                    f_references = False  # 参考文献を無視するようにフラグを変更
                    print('Detected References Section, Stopping Text Collection.')
                    print(text)
                    return title_text, keytext, extract_text_cleaned("\n".join(body_text))  # ここで本文抽出を終了
                continue

            # 本文のリストに追加
            if flag2:
                # print(text)
                body_text.append(text)
    
    print('end')
    return title_text, keytext, extract_text_cleaned("\n".join(body_text))


def test(filep):
    title_text, keytext,body_text = '', '', ''
    with open(filep, 'rb') as file:
        file_data = file.read()
    # file_data = file.read()
        pdf = BytesIO(file_data)
        title_text, keytext, body_text = extract_body_text3(pdf)
    
    print(title_text, keytext)
    print(body_text)
    pass

# 使用例
if __name__ == "__main__":
    dpath = './paper/'
    # filename = 'SiPhON提案論文.pdf'
    filename = 'sam2.pdf'

    test(dpath+filename)
    exit(0)

    title_text, keytext, body_text = extract_body_text2(dpath, filename)
    print(body_text)
