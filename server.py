from flask import Flask, request
from flask_cors import CORS
from flask_restful import Resource, Api
from flask_restful import reqparse
from sqlite3 import connect

app = Flask(__name__)
api = Api(app)
CORS(app, support_credentials=True)

class PostList(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("recipient", type=str, help="For who you send this message you")
        self.parser.add_argument("content", type=str, help="Content of your message")

    def _convert_to_beautiful_post(self, raw_post):
        return {"id": raw_post[0], "recipient": raw_post[1], "content": raw_post[2]}

    def get(self):
        connection = connect("secret_fans.db")

        # This line performs query and returns ResultObject
        query_result = connection.execute("SELECT rowid, recipient, content FROM post_tab;")
        raw_posts = query_result.fetchall() # Convert ResultObject to list of tuple
        return {"posts": [self._convert_to_beautiful_post(raw_post) for raw_post in raw_posts]}

    def post(self):
        # Parse the input data
        args = self.parser.parse_args()
        # Connect to database
        connection = connect("secret_fans.db")
        # This line performs query and returns ResultProxy
        query_result = connection.execute("INSERT INTO post_tab(`recipient`, `content`) VALUES (?, ?);", (args["recipient"], args["content"]))
        connection.commit()
        last_id = query_result.lastrowid
        return self._convert_to_beautiful_post([last_id, args["recipient"], args["content"]])


api.add_resource(PostList, "/post")

if __name__ == "__main__":
     app.run(port="8000")
