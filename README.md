# ニッチな専門技術ドキュメントQ&Aアシスタント

## 概要

このプロジェクトは、Brave Search APIとPythonのAIフレームワーク（Hugging Face Transformers, scikit-learn）を組み合わせた、特定のニッチな技術分野に特化したQ&Aアシスタントです。ユーザーが技術的な質問をすると、Web上の関連ドキュメントを検索し、そこから直接的な回答を抽出して提示します。

月間2,000クエリのBrave Search API無料プランと、運用・構築コストゼロの制約の中で、個人利用や小規模な情報探索を支援することを目指しています。

## 特徴

* **ニッチなQ&A**: 特定の技術ドメインに焦点を当てることで、より精度の高い回答を提供。
* **直接的な回答抽出**: Hugging Face TransformersのQ&Aモデルにより、ドキュメントから質問に対する直接的なテキストスパンを抽出。
* **関連ドキュメントの選定**: `scikit-learn`を用いて、検索結果から質問に最も関連性の高いドキュメントを効率的に特定。
* **Brave Search API活用**: 広範囲のWeb情報源、特にフォーラムやディスカッションからの情報を重視して検索。
* **コスト効率**: Brave Search APIの無料プランを利用し、アプリケーションはローカル環境で動作するため、運用コストはゼロ。
* **キャッシュ機能**: 過去の質問と回答、検索結果をローカルにキャッシュすることで、APIクエリ数を節約し、応答速度を向上。

## プロジェクト構造

```
qa_assistant/
├── main.py                     # アプリケーションのエントリポイント、CLIインターフェース
├── config.py                   # アプリケーション設定（APIキー、キャッシュパスなど）
├── brave_search_client.py      # Brave Search APIとの通信モジュール
├── web_page_parser.py          # WebページのHTMLパース＆テキスト抽出モジュール
├── relevance_evaluator.py      # scikit-learnを用いた関連度評価モジュール
├── qa_model_inferrer.py        # Hugging Face Transformersを用いたQ&amp;A推論モジュール
├── cache_manager.py            # SQLiteデータベースを用いたキャッシュ管理モジュール
├── models/                     # ダウンロードしたHugging Faceモデル保存用ディレクトリ
├── data/                       # キャッシュDBや一時データ保存用ディレクトリ
├── .env.example                # 環境変数の設定例
├── .gitignore                  # Gitの追跡から除外するファイル指定
├── requirements.txt            # プロジェクトの依存関係ライブラリリスト
└── README.md                   # このドキュメント
```

## セットアップ

このプロジェクトをローカルで実行するには、以下の手順に従ってください。

### 1. リポジトリのクローン

```bash
git clone [https://github.com/your-username/qa_assistant.git](https://github.com/your-username/qa_assistant.git)
cd qa_assistant
```

注: your-username はあなたのGitHubユーザー名に、qa_assistant.git は実際のプロジェクトリポジトリ名に置き換えてください。


### 2. Python仮想環境のセットアップ
プロジェクトの依存関係を隔離するために、仮想環境の使用を強く推奨します。

```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows
```

### 3. 必要なライブラリのインストール
requirements.txt に記載されているすべての依存ライブラリをインストールします。このファイルは次のステップで作成します。

```bash
pip install -r requirements.txt
```

### 4. Brave Search APIキーの設定

1. Brave Search APIダッシュボード (https://api-dashboard.search.brave.com/) で無料プランに登録し、APIキーを取得してください。
2. プロジェクトのルートディレクトリに `.env` というファイルを作成します。
3. `.env` ファイルに、取得したAPIキーを以下の形式で記述します。

    ```
    BRAVE_SEARCH_API_KEY="YOUR_BRAVE_API_KEY_HERE"
    ```

    **注:** `YOUR_BRAVE_API_KEY_HERE` をあなたの実際のAPIキーに置き換えてください。この `.env` ファイルは `.gitignore` でGitの追跡から除外されているため、安全に管理できます。

### 5. Hugging Face Q&amp;Aモデルのダウンロード

Q&Aモデルは初回実行時に自動的にダウンロードされますが、手動でキャッシュディレクトリを指定することも可能です。`models/` ディレクトリを使用するように設定します。

## 使用方法

### 質問の実行

仮想環境がアクティブな状態で、`main.py` スクリプトを実行し、質問を入力します。

```bash
python main.py
```

プロンプトが表示されたら、技術的な質問を入力してEnterキーを押してください。

**例**

```
質問を入力してください (終了するには'exit'または'quit'): PythonでPandasのDataFrameを結合するには？
```

アプリケーションはWebを検索し、関連情報を処理した後、抽出された回答と出典URLを表示します。

## 謝辞
1. Brave Search API
2. Hugging Face Transformers
3. scikit-learn
4. BeautifulSoup4
5. python-dotenv
