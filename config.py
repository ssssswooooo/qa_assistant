import os
from dotenv import load_dotenv

# .envファイルから環境変数をロード
# これにより、OSの環境変数にアクセスするのと同じように、.envファイルに定義された変数にアクセスできるようになる
load_dotenv()

# Brave Search APIキーの取得
# 環境変数 'BRAVE_SEARCH_API_KEY' が設定されていない場合、Noneを返す
BRAVE_SEARCH_API_KEY = os.getenv("BRAVE_SEARCH_API_KEY")

# キャッシュデータベースのパス
# プロジェクトルートのdataディレクトリ内にqa_cache.dbとして保存
CACHE_DB_PATH = os.path.join(os.path.dirname(__file__), 'data', 'qa_cache.db')

# Hugging Faceモデルのキャッシュディレクトリ
# プロジェクトルートのmodelsディレクトリ内に保存
HF_MODEL_CACHE_DIR = os.path.join(os.path.dirname(__file__), 'models')

# Brave Search APIの基本URL
BRAVE_API_BASE_URL = "https://api.search.brave.com/res/v1/web/search"

# Webページ取得時のタイムアウト秒数
WEB_REQUEST_TIMEOUT = 10

# Q&Aモデルの指定
# distilbert-base-cased-distilled-squad は比較的小さく、CPUでも動作しやすい
QA_MODEL_NAME = "distilbert-base-cased-distilled-squad"

# 検索結果からコンテンツを取得する最大URL数
# クエリ制限を考慮し、少なめに設定
MAX_CONTENT_URLS_TO_FETCH = 3

# Q&Aモデルに渡す関連性の高い段落の最大数
MAX_PARAGRAPHS_FOR_QA = 5