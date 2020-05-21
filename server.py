from flask import Flask, request
from flask_restful import Resource, Api
from flask_restful import reqparse
from json import dumps
from sqlalchemy import create_engine

db_connect = create_engine("sqlite:///secret_fans.db")
app = Flask(__name__)
api = Api(app)

class PostList(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("recipient", type=str, help="For who you send this message you")
        self.parser.add_argument("content", type=str, help="Content of your message")

    def _convert_to_beautiful_post(self, raw_post):
        return {"id": raw_post[0], "recipient": raw_post[1], "content": raw_post[2]}

    def get(self):
        conn = db_connect.connect() # Connect to database
        query_result = conn.execute("SELECT rowid, * FROM post_tab;") # This line performs query and returns ResultObject
        raw_posts = query_result.cursor.fetchall() # Convert ResultObject to list of list

        return {"posts": [self._convert_to_beautiful_post(raw_post) for raw_post in raw_posts]}
    
    def post(self):
        args = self.parser.parse_args() # Parse the data
        
        conn = db_connect.connect() # Connect to database
        query_result = conn.execute("INSERT INTO post_tab(`recipient`, `content`) VALUES ('{}', '{}');".format(args["recipient"], args["content"])) # This line performs query and returns ResultProxy
        last_id = query_result.lastrowid

        return self._convert_to_beautiful_post([last_id, args["recipient"], args["content"]])


api.add_resource(PostList, "/post")

if __name__ == "__main__":
     app.run(port="8000")