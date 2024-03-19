from flask import Flask, request

from gpx_processor import gpx_driver

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        uploaded_gpx_text = file.read().decode('utf-8')
        uploaded_gpx_driver = gpx_driver.GPXDriver()
        uploaded_gpx_driver.open_string(uploaded_gpx_text)
        uploaded_gpx_title = uploaded_gpx_driver.get_name()

        return '''
        <!doctype html>
        <title>Content of the text file</title>
        <h1>Content of the text file</h1>
        <pre>{}</pre>
        '''.format(uploaded_gpx_title)
    return '''
    <!doctype html>
    <title>Upload a text file</title>
    <h1>Upload a text file and display its content</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

if __name__ == '__main__':
    app.run(debug=True)