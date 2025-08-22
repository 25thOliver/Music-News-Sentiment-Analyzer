from pymongo import MongoClient

def test_connection():
    try:
        # connect to mongodb container (use same creds you passed in docker run)
        client = MongoClient("mongodb://admin:admin123@localhost:27017/")

        # select the database
        db = client["music_news_db"]

        # test inserting a document
        result = db.articles.insert_one({"title": "Docker Test", "content": "Connected successfully!"})

        print("✅ Inserted document ID:", result.inserted_id)

        # test fetching documents
        for doc in db.articles.find():
            print("📄", doc)

        print("\nMongoDB connection test passed ✅")

    except Exception as e:
        print("❌ Connection failed:", e)


if __name__ == "__main__":
    test_connection()
