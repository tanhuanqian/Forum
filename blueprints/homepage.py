from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, g, jsonify
import os
from usermodel import PostModel, CommentModel
from .forms import ContentForm
from werkzeug.utils import secure_filename
from extensions import db

bp = Blueprint("homepage", __name__, url_prefix="/")

@bp.route("/")
def home():
    if not g.user:
        return render_template("index.html")
    else:
        posts = PostModel.query.order_by(PostModel.create_time.desc()).all()
        return render_template("forum_home.html", posts=posts)
    
@bp.route('/create', methods=['GET', 'POST'])
def create():
    form = ContentForm()
    
    if request.method == 'POST':
        form = ContentForm(request.form, request.files)
        if form.validate():
            title = form.title.data
            content = form.content.data
            new_post = PostModel(title=title, content=content, author=g.user)

            image = request.files.get('image')
            if image:
                upload_folder = os.path.join(current_app.root_path, 'static/uploads')
                if not os.path.exists(upload_folder):
                    os.makedirs(upload_folder)  # 创建目录
                filename = secure_filename(image.filename)
                image_path = os.path.join(upload_folder, filename)
                image.save(image_path)
                new_post.image_path = f'uploads/{filename}'  # Save path in 'uploads/filename' format
            else:
                new_post.image_path = None

            db.session.add(new_post)
            db.session.commit()
            flash("Post created successfully!", "success")
            return redirect(url_for("homepage.home"))

    return render_template('create_post.html', form=form)

@bp.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    if query:
        # 假设您在PostModel中有一个方法可以搜索帖子
        results = PostModel.query.filter(PostModel.title.ilike(f'%{query}%')).all()  # 根据标题搜索
    else:
        results = []

    return render_template('search_results.html', query=query, results=results)

@bp.route("/post/<int:post_id>", methods=["GET", "POST"])
def view_post(post_id):
    post = PostModel.query.get_or_404(post_id)
    if request.method == "POST":
        content = request.form.get("comment_content")
        if content:
            new_comment = CommentModel(content=content, post_id=post.id, user_id=g.user.id)
            db.session.add(new_comment)
            db.session.commit()
            flash("评论已添加！")
            return redirect(url_for("homepage.view_post", post_id=post_id))
        else:
            flash("评论不能为空！")
    comments = CommentModel.query.filter_by(post_id=post.id).order_by(CommentModel.create_time.asc()).all()
    return render_template("post_detail.html", post=post, comments=comments)

@bp.route('/post/<int:post_id>/vote', methods=['POST'])
def vote(post_id):
    post = PostModel.query.get(post_id)
    
    if post is None:
        return jsonify({'error': 'Post not found'}), 404
    
    data = request.json
    action = data.get('action')
    
    if action == 'upvote':
        post.vote_count = (post.vote_count or 0) + 1  # 增加投票计数
    elif action == 'downvote':
        post.vote_count = (post.vote_count or 0) - 1  # 减少投票计数
    
    # 保存更新后的 post
    db.session.commit()
    
    return jsonify({'vote_count': post.vote_count})

@bp.route('/post/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    post = PostModel.query.get(post_id)
    if post is None:
        return jsonify({'error': 'Post not found'}), 404
    
    db.session.delete(post)
    db.session.commit()
    return jsonify({'message': 'Post deleted successfully'})

@bp.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
def edit_post(post_id):
    post = PostModel.query.get(post_id)
    if post is None:
        return jsonify({'error': 'Post not found'}), 404

    if request.method == 'POST':
        data = request.form
        post.title = data.get('title')
        post.content = data.get('content')
        db.session.commit()
        return redirect(url_for('homepage.view_post', post_id=post.id))

    return render_template('edit_post.html', post=post)  # 创建一个单独的模板用于编辑贴文