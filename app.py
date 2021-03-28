import route
import bmr
from flask import Flask
app = Flask(__name__)

bmr.main()

app.add_url_rule('/', view_func=route.hello_world)
app.add_url_rule('/<name>', view_func=route.name)
app.add_url_rule('/simplequery/<query>', view_func=route.SimpleQuery)

if __name__ == "__main__":
    app.run(debug=True)