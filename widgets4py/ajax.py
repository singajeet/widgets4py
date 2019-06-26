from flask import Flask


app = Flask(__name__)


@app.route("/")
def hello():
    return """<html>
                <head>
                    <title>ajax test</title>
                    <script src="https://code.jquery.com/jquery-3.4.1.min.js" ></script>
                </head>
                <body>
                    <input type="button" id="test" name="test" value="Push"
                    onclick="
                        $.ajax({
                            url: 'test.abc',
                            success: function(status){alert('success');},
                            error: function(status){alert('failed');}
                        });
                        "
                    />
                </body>
            </html>
            """
