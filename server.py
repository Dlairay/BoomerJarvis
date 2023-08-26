from flask import Flask, redirect, url_for, render_template, request
import re
import os
from dotenv import load_dotenv
import openai
from translator import translate_text,detect_language

load_dotenv()
openai.api_key= os.getenv("OPENAI_APIKEY")

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def home():

    system_message = """
    you are an informative assistant to help Technology illiterate elderly to navigate the internet. 
    your responses should be as simple as possible but useful. 
    you will provide step by step guidance on how to go about achieving a task prompted by the user.
    """

    while(1):
        if request.method == 'GET':
            return render_template("index.html")
        else:
        # get data
            qn = request.form["question"]

            language = detect_language(qn)
            if language == "en":
                translated_input = qn
            else:
                translated_input = translate_text(target="en",text=qn)

            prompt = translated_input

            
            new_message = {"role": "user", "content":prompt}
            message_log = [
                    {"role": "system", "content": system_message},
                    ]
            message_log.append(new_message)

            
            completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=message_log
                )
            if language == "en":
                translated_output = completion.choices[0].message["content"]
            else: 
                translated_output = translate_text(target=language,text=completion.choices[0].message["content"])
                
            print(translated_output)
            fullAns = translated_output
            finalAns = re.split("\n\n", fullAns)
            return render_template("index.html", qn=qn, answer=finalAns)
    
if __name__ == "__main__":
	app.run(debug=True)
