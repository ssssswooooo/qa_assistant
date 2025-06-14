import sqlite3
import os
import json # 検索結果のJSONデータを保存するために使用

class CacheManager:
    """
    アプリケーションのキャッシュ管理を担当するクラス。
    SQLiteデータベースを使用して、質問、検索結果、Webページコンテンツ、回答を保存・取得する。
    """
    def __init__(self, db_path):
        """
        CacheManagerを初期化します。
        データベースファイルが存在しない場合は作成し、テーブルを初期化します。

        Args:
            db_path (str): SQLiteデータベースファイルのパス。
        """
        self.db_path = db_path
        self._initialize_db()

    def _initialize_db(self):
        """
        データベースを初期化し、必要なテーブルを作成します。
        テーブルが存在しない場合のみ作成されます。
        """
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # 'queries' テーブル: ユーザーの質問と関連するメタデータを保存
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS queries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    question TEXT UNIQUE NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                );
            ''')

            # 'search_results' テーブル: Brave Search APIからの検索結果を保存
            # result_dataはJSON形式で保存
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS search_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    query_id INTEGER NOT NULL,
                    brave_response_json TEXT NOT NULL,
                    FOREIGN KEY (query_id) REFERENCES queries(id)
                );
            ''')

            # 'web_contents' テーブル: 取得したWebページの本文コンテンツを保存
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS web_contents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT UNIQUE NOT NULL,
                    content TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                );
            ''')

            # 'answers' テーブル: 抽出された回答と、それが関連するクエリ、WebコンテンツのURLを保存
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS answers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    query_id INTEGER NOT NULL,
                    answer_text TEXT NOT NULL,
                    source_url TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (query_id) REFERENCES queries(id)
                );
            ''')

            conn.commit()
            print(f"Database initialized or already exists at: {self.db_path}")

        except sqlite3.Error as e:
            print(f"Database initialization error: {e}")
        finally:
            if conn:
                conn.close()

    def get_cached_answer(self, question):
        """
        指定された質問に対するキャッシュされた回答を取得します。

        Args:
            question (str): ユーザーからの質問。

        Returns:
            tuple or None: (answer_text, source_url) のタプル、またはキャッシュがない場合はNone。
        """
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                SELECT a.answer_text, a.source_url
                FROM answers a
                JOIN queries q ON a.query_id = q.id
                WHERE q.question = ?
                ORDER BY a.timestamp DESC
                LIMIT 1;
            ''', (question,))
            result = cursor.fetchone()
            return result
        except sqlite3.Error as e:
            print(f"Error getting cached answer: {e}")
            return None
        finally:
            if conn:
                conn.close()

    def cache_qa_data(self, question, brave_response_json, web_contents_data, answer_text, source_url):
        """
        質問、Brave Searchの結果、Webページコンテンツ、抽出された回答をキャッシュします。

        Args:
            question (str): ユーザーからの質問。
            brave_response_json (dict): Brave Search APIからの生JSONレスポンス。
            web_contents_data (list): [(url, content), ...] 形式のWebページコンテンツのリスト。
            answer_text (str): 抽出された回答テキスト。
            source_url (str): 回答の出典元のURL。
        """
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # 1. 'queries' テーブルに質問を挿入（または既存IDを取得）
            cursor.execute('INSERT OR IGNORE INTO queries (question) VALUES (?)', (question,))
            cursor.execute('SELECT id FROM queries WHERE question = ?', (question,))
            query_id = cursor.fetchone()[0]

            # 2. 'search_results' テーブルにBrave Searchの生レスポンスを挿入
            cursor.execute('''
                INSERT INTO search_results (query_id, brave_response_json)
                VALUES (?, ?)
            ''', (query_id, json.dumps(brave_response_json)))

            # 3. 'web_contents' テーブルにWebページコンテンツを挿入
            for url, content in web_contents_data:
                cursor.execute('''
                    INSERT OR IGNORE INTO web_contents (url, content)
                    VALUES (?, ?)
                ''', (url, content))

            # 4. 'answers' テーブルに回答を挿入
            cursor.execute('''
                INSERT INTO answers (query_id, answer_text, source_url)
                VALUES (?, ?, ?)
            ''', (query_id, answer_text, source_url))

            conn.commit()
            print("QA data successfully cached.")

        except sqlite3.Error as e:
            print(f"Error caching QA data: {e}")
            # エラー発生時はロールバック
            if conn:
                conn.rollback()
        finally:
            if conn:
                conn.close()

    def get_cached_brave_response(self, question):
        """
        指定された質問に対するキャッシュされたBrave Searchの生レスポンスを取得します。

        Args:
            question (str): ユーザーからの質問。

        Returns:
            dict or None: Brave Searchの生JSONレスポンス辞書、またはキャッシュがない場合はNone。
        """
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                SELECT sr.brave_response_json
                FROM search_results sr
                JOIN queries q ON sr.query_id = q.id
                WHERE q.question = ?
                ORDER BY sr.id DESC
                LIMIT 1;
            ''', (question,))
            result = cursor.fetchone()
            if result:
                return json.loads(result[0])
            return None
        except sqlite3.Error as e:
            print(f"Error getting cached Brave response: {e}")
            return None
        finally:
            if conn:
                conn.close()

    def get_cached_web_contents(self, urls):
        """
        指定されたURLリストに対するキャッシュされたWebコンテンツを取得します。

        Args:
            urls (list): 取得したいWebコンテンツのURLリスト。

        Returns:
            dict: {url: content} の形式で、キャッシュされたコンテンツを返します。
                  キャッシュされていないURLは含まれません。
        """
        conn = None
        cached_contents = {}
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            for url in urls:
                cursor.execute('SELECT content FROM web_contents WHERE url = ?', (url,))
                result = cursor.fetchone()
                if result:
                    cached_contents[url] = result[0]
            return cached_contents
        except sqlite3.Error as e:
            print(f"Error getting cached web contents: {e}")
            return {}
        finally:
            if conn:
                conn.close()

# モジュールがインポートされたときにデータベースを初期化
# これはmain.pyでCacheManagerをインスタンス化する際に自動的に行われる
# または、config.pyのCACHE_DB_PATHを使って直接初期化を呼び出すことも可能
# 例: cache_manager_instance = CacheManager(config.CACHE_DB_PATH)