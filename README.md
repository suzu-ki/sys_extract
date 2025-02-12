## 英語論文から、専用語（っぽい単語）リストを抽出するシステム

### セットアップ
ターミナルに以下の順番でコマンドを入力

```
python -m venv env
```

```
. env/bin/activate
```

```
pip install -r requirements.txt
```

```
python -m spacy download en_core_web_sm
```

### 実行
```
streamlit run app.py
```
自動でブラウザに立ち上がらなかったら、ターミナルに記述されるLocal URLにアクセス

## 終了
システム終了：
control + C

環境終了：
```
deactivate
```

### 実装環境
MacOS: 14.5
Python: 3.10.7
pdfminer.six: 20240706
spacy: 3.8.4
streamlit: 1.42.0
