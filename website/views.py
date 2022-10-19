from flask import Blueprint, render_template, redirect, request, flash, url_for
from flask_login import login_required, current_user
from . import db
from .models import Snippet, User, Profile
import validators
import random
import string

views = Blueprint('views', __name__)

@views.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('views.snippets'))
    else:
        return render_template('home.html', user=current_user)


@views.route('/snippets', methods=['GET', 'POST']) # DONE
@login_required
def snippets():
    if request.method == 'POST':
        try:
            if request.form['add_snippet'] == "Add Code Snippet":
                return redirect(url_for('views.edit_snippet'))
        except:
            pass
    return render_template("snippets.html", user=current_user)

@views.route('editor', methods=['GET', 'POST'])
@login_required
def edit_snippet():
    if request.method == 'POST':
        # try:
        if request.form['save'] == "Save": # Saves to db
            title = request.form['title']
            paste_content = request.form['paste_content']
            lang = request.form['lang']
            print(lang)
            if paste_content == "":
                flash("Paste Something First!", category='error')
                return redirect(url_for('views.edit_snippet'))
                
            else:
                if title == "":
                    title = "New Paste"
                url_id = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(5))
                snippet = Snippet(url_id=url_id, title=title, content=paste_content, lang=lang, user_id = current_user.id)
                db.session.add(snippet)
                db.session.commit()
                flash('New Paste Created!', category='success')
                return redirect(url_for('views.snippets'))
        # except:
        #     flash("Something went wrong!", category='error')
    return render_template("snippet_editor.html", user=current_user)

@views.route('/delete/<int:id>') # DONE
@login_required
def delete_link(id):
    snippet_to_delete = Snippet.query.get_or_404(id)
    try:
        db.session.delete(snippet_to_delete)
        db.session.commit()
        return redirect(url_for('views.snippets'))
    except:
        flash('Try again later.', category='error')

@views.route('/edit/<int:id>', methods=['POST', 'GET'])
@login_required
def update_snippet(id):
    snippet_to_update = Snippet.query.get_or_404(id)
    if request.method == 'POST':
        snippet_to_update.content = request.form['paste_content']
        snippet_to_update.title = request.form['title']
        try:
            db.session.commit()
            return redirect('/')
        except:
            flash("An error has occured!", category='error')
    
    return render_template('update.html', snippet=snippet_to_update, user=current_user)


@views.route('/@<username>') # not needed for now, pls ignore
def show_user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('show_user.html', user=user)

@views.route('/<url_id>')
def show_snippet(url_id):
    snippet = Snippet.query.filter_by(url_id=url_id).first_or_404()
    return render_template('show_snippet.html', snippet=snippet)