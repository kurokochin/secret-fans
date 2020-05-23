from flask import Flask, request
from flask_cors import CORS
from flask_restful import Resource, Api
from flask_restful import reqparse
from sqlite3 import connect

app = Flask(__name__)
api = Api(app)
CORS(app, support_credentials=True)

def _convert_to_beautiful_post(raw_post):
    return {"id": raw_post[0], "recipient": raw_post[1], "content": raw_post[2]}

def _convert_to_beautiful_comment(raw_comment):
    return {"id": raw_comment[0], "post_id": raw_comment[1], "content": raw_comment[2]}

class PostList(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("recipient", type=str, help="For who you send this message you")
        self.parser.add_argument("content", type=str, help="Content of your message")

    def get(self):
        # Connecto to database
        connection = connect("secret_fans.db")

        # This line performs query and returns ResultProxy
        query_result = connection.execute("SELECT rowid, recipient, content FROM post_tab;")

        # Convert ResultProxy to list of tuple
        raw_posts = query_result.fetchall()

        # Parse and return the result
        return {"posts": [_convert_to_beautiful_post(raw_post) for raw_post in raw_posts]}

    def post(self):
        # Parse the input data
        args = self.parser.parse_args()

        # Connect to database
        connection = connect("secret_fans.db")

        # This line performs query and returns ResultProxy
        query_result = connection.execute("INSERT INTO post_tab(`recipient`, `content`) VALUES (?, ?);", (args["recipient"], args["content"]))
        connection.commit()

        # Get the last inserted post id
        last_id = query_result.lastrowid

        # Parse and return the result
        return _convert_to_beautiful_post([last_id, args["recipient"], args["content"]])

class PostDetail(Resource):
    def get(self, post_id):
        # Connect to database
        connection = connect("secret_fans.db")

        # This line performs query and returns ResultProxy
        query_result = connection.execute("SELECT rowid, recipient, content FROM post_tab WHERE rowid=?;", (post_id,))
        
        # Get the first post
        raw_post = query_result.fetchone()

        # Parse and return the result
        return {"post": _convert_to_beautiful_post(raw_post)}

class CommentList(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("content", type=str, help="Content of your comment")

    def get(self, post_id):
        # Connecto to database
        connection = connect("secret_fans.db")

        # This line performs query and returns ResultProxy
        query_result = connection.execute("SELECT rowid, post_id, content FROM comment_tab WHERE post_id=?;", (post_id,))

        # Convert ResultProxy to list of tuple
        raw_comments = query_result.fetchall()

        # Parse and return the result
        return {"comments": [_convert_to_beautiful_comment(raw_comment) for raw_comment in raw_comments]}

    def post(self, post_id):
        # Parse the input data
        args = self.parser.parse_args()

        # Connect to database
        connection = connect("secret_fans.db")

        # This line performs query and returns ResultProxy
        query_result = connection.execute("INSERT INTO comment_tab(`post_id`, `content`) VALUES (?, ?);", (post_id, args["content"]))
        connection.commit()

        # Get the last inserted post id
        last_id = query_result.lastrowid

        # Parse and return the result
        return _convert_to_beautiful_comment([last_id, post_id, args["content"]])

api.add_resource(PostList, "/posts")
api.add_resource(PostDetail, "/posts/<int:post_id>")
api.add_resource(CommentList, "/comments/<int:post_id>")

if __name__ == "__main__":
     app.run(port="8000")
