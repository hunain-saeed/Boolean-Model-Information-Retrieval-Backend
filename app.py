import route
import bmr
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

bmr.main()

app.add_url_rule('/', view_func=route.hello_world)
app.add_url_rule('/gettitle', view_func=route.gettitle)
app.add_url_rule('/booleanquery/<query>', view_func=route.queryType)

if __name__ == "__main__":
    app.run(debug=True)