from myproject import app  # ,socketio
from flask import Response, render_template


@app.errorhandler(404)
def not_found(e):
    resp = Response(render_template('404.html'), status=404)
    return resp

# sad 
if __name__ == '__main__':
    # socketio.run(app)
    app.run(debug=True)
