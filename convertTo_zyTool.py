from flask import Flask, render_template, request, make_response

def createJSFile(tool_name, html, css, js):
    html = html.replace('\\','\\\\').replace('"','\\"').replace("\n","\\n")
    css = css.replace('\\','\\\\').replace('"','\\"').replace("\n","\\n")
    cap_first_letter = tool_name[0:1].capitalize() + tool_name[1:]
    js_str = ""
    js_str += js + "\n"
    js_str += "function init" + cap_first_letter + "() {\n"
    js_str += "    function loadHTMLandCSS() {\n"
    js_str += "        var html = \"" + html + "\"\n"
    js_str += "        var css = \"<style>" + css + "</style>\"\n"
    js_str += "        $(\"#" + tool_name + "\").html(css + html)\n"
    js_str += "    }\n\n"
    js_str += "    loadHTMLandCSS();\n"
    js_str += "}\n"
    
    return js_str

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        # 1) get the text area data
        tool_name = request.form['toolName']
        css = request.form['cssText'].replace('\r\n', '\n').replace('images/pics/','/images/pics/')
        js = request.form['jsText'].replace('\r\n', '\n').replace('images/pics/','/images/pics/')
        html = request.form['htmlText'].replace('\r\n', '\n').replace('images/pics/','/images/pics/')
        
        # 2) create the js
        jsFile = createJSFile(tool_name, html, css, js)
        
        # 3) send js
        response = make_response(jsFile)
        response.headers['Content-Disposition'] = 'attachment; filename=' + tool_name + '.js'
        return response
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run()
