import logging
from datetime import datetime
from whcfix.logic.matches import Matches
from whcfix.data.models import MatchReport, Post
from flask import render_template, request, Blueprint, abort
from whcfix.data.database import get_db
from flask import url_for, flash, redirect, session
from whcfix.utils import save_image_from_form

news = Blueprint('news', __name__, template_folder='whcfix/templates')


@news.route("/select_match_for_match_report/<team>/")
def select_match_for_match_report(team):
    matches = Matches().get_matches(lambda m: m.doesFeature(team))
    return render_template('select_match_for_match_report.html',
                           matches=matches, team=team)


@news.route('/submit_match_report/<home>/<away>/<date>/<time>/',
            methods=['GET', 'POST'])
def submit_match_report(home, away, date, time):
    if request.method == 'POST':
        title = "Match Report: %s vs %s" % (home, away)
        body = request.form['body']
        image_file_name = save_image_from_form(request.form, 'image')
        match_report = MatchReport()
        match_report.is_published = False
        match_report.title = title
        match_report.home = home
        match_report.away = away
        match_report.push_back = datetime.strptime("%s %s" % (date, time),
                                                   "%d-%m-%y %H:%M")
        match_report.body = body
        match_report.image_file_name = image_file_name
        with get_db() as db:
            db.add(match_report)
        flash("Thank you for your submission.")
        return redirect(url_for('news.news_home'))
    else:
        return render_template("submit_match_report.html", home=home,
                               away=away, date=date, time=time)


@news.route('/news/post/<int:post_id>/', methods=['GET', 'POST'])
def post_detail(post_id):
    with get_db() as db:
        post = db.query(Post).filter(Post.id == post_id).first()
        if post:
            logging.debug("Found post with id=%s" % post.id)
            if request.method == 'POST':
                logging.debug("POST recieved")
                post.title = request.form['title']
                post.body = request.form['body']
                post.is_published = 'published' in request.form
                if 'published' in request.form:
                    post.publish()
                post.image_file_name = save_image_from_form(request.form,
                                                            'image')
                flash("Successfully Saved!")
                return redirect(url_for('news.post_detail', post_id=post.id))
            else:
                logging.debug("GET recieved")
                return render_template('post_detail.html', post=post)
        else:
            abort(404)


@news.route("/delete_post/<int:post_id>/")
def delete_post(post_id):
    kwargs = request.args.to_dict()
    with get_db() as db:
        post = db.query(Post).filter(Post.id == post_id).first()
        if not session['logged_in']:
            abort(401)
        elif not post:
            abort(404)
        elif 'confirmed' not in kwargs:
            template = "You're about to delete the post: %s. Are you sure?"
            message = template % (post.title,)
            action_message = "Delete Post."
            return render_template('confirm.html',
                                   message=message,
                                   action_message=action_message,
                                   post=post)
        else:
            db.delete(post)
            flash("Post deleted.")
            return redirect(url_for("news.news_home"))


def lookup_and_do(Model, id, action, redirect_url, redirect_parameters):
    if not session['logged_in']:
        abort(401)
    else:
        with get_db() as db:
            instance = db.query(Model).filter(Model.id == id).first()
            if instance:
                action(instance)
                return redirect(url_for("news." + redirect_url,
                                        **redirect_parameters))
            else:
                abort(404)


@news.route("/unpublish_post/<int:post_id>/")
def unpublish_post(post_id):
    return lookup_and_do(Post, post_id,
                         lambda p: p.unpublish(),
                         'news_home', {'post_id': post_id})


@news.route("/publish_post/<int:post_id>/")
def publish_post(post_id):
    return lookup_and_do(Post, post_id,
                         lambda p: p.publish(),
                         'news_home', {'post_id': post_id})


@news.route("/news/")
def news_home():
    with get_db() as db:
        posts = db.query(Post).order_by(Post.first_published_date,
                                        Post.id).all()[::-1]
        return render_template("news.html", posts=posts)


@news.route("/news/new/", methods=['POST'])
def add_news():
    post = Post()
    post.title = request.form['title']
    post.body = request.form['body']
    post.is_published = 'published' in request.form
    if 'published' in request.form:
        post.publish()
    post.image_file_name = save_image_from_form(request.form, 'image')
    with get_db() as db:
        db.add(post)
    flash("New entry was successfully posted!")
    return redirect(url_for('news.news_home'))
