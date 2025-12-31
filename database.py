import sqlite3
from content_bot.models.news import News


class DataBase:
    def __init__(self, db_name="news_agent.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):

        sql = """
          CREATE TABLE IF NOT EXISTS news(
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          title TEXT,
          content TEXT,
          url TEXT UNIQUE,
          source TEXT,
          date TEXT,
          summary TEXT,
          sentiment TEXT,
          author TEXT
          
          
          )

        """
        self.cursor.execute(sql)

        self.conn.commit()

    def add_news(self, news: News):

        sql = """INSERT OR IGNORE INTO news 
                 (title, content, url, source, author,date,summary,sentiment) 
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""

        self.cursor.execute(
            sql,
            (
                news.title,
                news.content,
                news.url,
                news.source,
                news.author,
                "2025-12-24",
                None,
                None,
            ),
        )

        self.conn.commit()

    def update_new_analysis(self, news_id, summary, sentiment):
        sorgu = """UPDATE news
                SET summary= ? ,sentiment=?
                WHERE id=?
            """

        self.cursor.execute(sorgu, (summary, sentiment, news_id))

        self.conn.commit()
        print("Güncelleme başarı ile tamamlandı")

    def get_unprocessed_news(self):
        query = """SELECT id,title,content 
                 FROM news
                 WHERE summary IS NULL"""
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_analyzed_news(self):
        self.cursor.execute(
            """
                            SELECT title,summary,sentiment
                            FROM news
                            WHERE summary IS NOT NULL"""
        )

        rows = self.cursor.fetchall()
        news_list = []
        for row in rows:
            news_list.append({"title": row[0], "summary": row[1], "sentiment": row[2]})

        return news_list

    def close(self):
        self.conn.close()
