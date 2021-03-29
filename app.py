import route
import bmr
from flask import Flask
app = Flask(__name__)

bmr.main()

app.add_url_rule('/', view_func=route.hello_world)
app.add_url_rule('/simplequery/<query>', view_func=route.SimpleQuery)
app.add_url_rule('/booleanquery/<query>', view_func=route.queryType)

if __name__ == "__main__":
    app.run(debug=True)