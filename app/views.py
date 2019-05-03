from app import app
from flask import render_template, request, redirect, url_for, jsonify,flash
from app.forms import DocsForm
from werkzeug.utils import secure_filename
import os
import nltk
import json

"""
Making use of NLTK and collections library, 
to serve requests for finding most occuring words in a
document(s). Simply upload your documents.
"""
#show results
@app.route('/show',methods=['GET', 'POST'])
def show():
    result = []
    files = json.loads(request.args.get('names') )
    for name in files:
        filename = os.path.join(app.config['UPLOAD_FOLDER'], name)
        with open(filename) as f:
            doc = f.read()
        words = to_words(doc)
        sentences_ = to_sentences(doc)
        most = most_occur(words)
        occurs = occurs_in(most,sentences_)
        result.append({'filename':name,'word':most, 'sentences':occurs})
    return render_template('results.html', results = result)

# split documents into words and
# perform some cleaning routines
def to_words(doc):
    from nltk.tokenize import word_tokenize
    tokens = word_tokenize(doc)
    # convert to lower case
    tokens = [w.lower() for w in tokens]
    # remove punctuation from each word
    import string
    table = str.maketrans('', '', string.punctuation)
    stripped = [w.translate(table) for w in tokens]
    # remove all tokens that are not alphabetic
    words = [word for word in stripped if word.isalpha()]
    # filter out stop words
    from nltk.corpus import stopwords
    stop_words = set(stopwords.words('english'))
    words = [w for w in words if not w in stop_words|{'nt','enough','promise','let','know','us'}]
 
    return words

# break the document down to sentences
def to_sentences(doc):
    # split into sentences
    from nltk import sent_tokenize
    sentences = sent_tokenize(doc)
    return sentences

# find the most occuring word in a collection
def most_occur(words):
    from collections import Counter  
    Counter = Counter(words) 
    return Counter.most_common()[0][0]

# select sentences which has the word in them
def occurs_in(word,sentences):
    res = []
    for s in sentences:
        if s.lower().find(str(word)) == -1:
            pass
        else:
            res.append(s)
    return res 

#upload your documents
@app.route('/', methods=['GET', 'POST'])
def upload():
    form = DocsForm()
    if form.validate_on_submit():
        print('file validates')
        file_filenames = []
        names = []
        for files in form.files.data:
            if allowed_file(files.filename):
                files_filenames = secure_filename(files.filename)
                names.append(files_filenames)
                files.save(os.path.join(app.config['UPLOAD_FOLDER'], files_filenames))
            else:
                flash('Upload only text files')
                return render_template('upload.html', form=form)
        return redirect(url_for('show', names=json.dumps(names)))
    flash('Upload only text files')
    return render_template('upload.html', form=form)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']