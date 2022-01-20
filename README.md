<h1 align="center">PDF教材販売サイト</h1>

<details open="open">
  <summary>目次</summary>
  <ol>
    <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
  </ol>
</details>

## Getting Started
開発を始めるための手順を説明します。

### Prerequisites
開発の推奨環境は以下のとおりです。

* Python 3.8 以上

### Installation

1. `venv`の作成

```shell
python -m venv venv
```

2. 関連パッケージのインストール

```shell
pip install -r requirements.txt
```

3. サーバーの起動

```shell
python app.py
```

4. ブラウザで[http://localhost:5000](http://localhost:5000)にアクセス

5. dbの作成  
  pythonの対話型シェルを開き以下のコマンドを入力
```python
>>> from app import db
>>> db.create_all()
```
  dbを更新する時は、一旦`app.db`を削除してもう一度上のコマンドを入力！


