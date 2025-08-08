from __init__ import app, BlogPost, User, Contact, db, os
from flask import render_template, request, redirect, url_for, flash, abort
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from json import load

# Load configuration parameters from config.json
with open("config.json","r") as c:
	params=load(c)["params"]

@app.route('/')
def home():
    page = request.args.get('page', 1, type=int)
    per_page = params["no_of_per_page"]  # Adjust as needed
    posts = BlogPost.query.order_by(BlogPost.date_posted.desc()).paginate(page=page, per_page=per_page, error_out=False)
    return render_template('index.html', posts=posts, params=params)

@app.route("/contact")
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        contact = Contact(name=name,email=email,message=message)
        db.session.add(contact)
        db.session.commit()
    
    return render_template('contact.html',params=params)
	
@app.route("/about")
def about():
	return render_template('about.html',params=params)

@app.route('/post/<int:post_sno>')
def post(post_sno):
    post = BlogPost.query.get(post_sno)
    return render_template('post.html', post=post, params=params)
    
@app.route("/login",methods=["GET","POST"])
def login():
	if request.method == 'POST':
	       user = request.form['username']
	       pas = request.form['password']
	       remember = request.form['remember']
	       
	       usern = User.query.filter_by(username=user).first()
	       if usern and check_password_hash(usern.password, pas):
	       	login_user(usern,remember=remember=="on")
	       return redirect('/admin')
	return render_template("login.html",params=params)

@app.route("/register",methods=["GET","POST"])
def register():
    if request.method == 'POST':
        email = request.form['emailId']
        usern = request.form['username']
        pas = request.form['password']
        remember = request.form['remember']
        confirm_password = request.form['confirm_password']
	       
	    # Check if the username is already taken
        existing_user = User.query.filter_by(username=usern).first()
        if existing_user:
            flash('Username already taken. Please choose a different username.', 'danger')
            return redirect('/register')
        
        if pas != confirm_password:
	        flash('Passwords do not match. Please try again.', 'danger')
	        return redirect('/register')

        # Hashing a password
        hashed_password = generate_password_hash(pas, method='pbkdf2:sha256')
        user = User(email=email,username=usern,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        
        login_user(user,remember=remember=="on")
        return redirect('/admin')
    return render_template("register.html",params=params)

@app.route('/admin')
@login_required
def admin():
    return render_template("admin.html", params=params)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        # Handle profile photo upload
        if 'profile_photo' in request.files:
            file = request.files['profile_photo']
            if file.filename != current_user.userImg:
                filename = "userImg/" +  secure_filename(file.filename)
                file.save(os.path.join("/storage/emulated/0/Blog/static/", filename))
                # Save the filename to the user's profile in the database
                user = User.query.filter_by(id=current_user.id).first()
                user.userImg = filename
                user.username = request.form.get('username')
                db.session.commit()
        
        return redirect(url_for('admin'))

    return render_template('edit_profile.html',params=params)

@app.route('/edit/<int:sno>', methods=['GET','POST'])
def edit(sno):
    if(request.method=='POST'):
        #slug = request.form.get('slug')
        title = request.form.get('title')
        file = request.files['thumbnail']
        con = request.form.get('content')
        thumb=f"thumb/{file.filename}"
        Path=app.config['UPLOAD_THUMB']
        if not os.path.isfile(Path):
        	file.save(os.path.join(Path, secure_filename(thumb)))
        if sno==0:
        	post=BlogPost(title=title,content=con,thumb=thumb,author=current_user)
        	db.session.add(post)
        	db.session.commit()
        else:
        	post=BlogPost.query.filter_by(sno=sno).first()
        	#post.slug=slug
        	post.title=title
        	post.thumb=thumb
        	post.content=con
        	db.session.commit()
        return redirect("/admin")
    post=BlogPost.query.filter_by(sno=sno).first()
    return render_template('Edit.html',post=post,sno=sno,params=params)

@app.route('/delete/<int:post_sno>')
@login_required
def delete(post_sno):
    post = BlogPost.query.get_or_404(post_sno)

    # Check if the current user is the author of the post
    if post.author != current_user:
        abort(403)  # Forbidden
        
    file_path=app.config['UPLOAD_THUMB']+post.thumb
    if os.path.isfile(file_path):
    	os.remove(file_path)
    db.session.delete(post)
    db.session.commit()

    flash('Your blog post has been deleted!', 'success')
    return redirect('/admin')

@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect("/login")