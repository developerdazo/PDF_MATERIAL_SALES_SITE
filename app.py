import os
from datetime import datetime

from flask import Flask, render_template, request, flash, url_for, send_from_directory, redirect

# flaskのインタスタンスを作成
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

from sqlalchemy import func

app = Flask(__name__)

# dbの設定
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['UPLOAD_DIR'] = os.getenv('UPLOAD_DIR_PATH', './upload')
app.config['SECRET_KEY'] = 'Kamesuta'
db = SQLAlchemy(app)


# モデルの定義
class Product(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(255), default="名無し")
	path = db.Column(db.String(255), nullable=False)
	price = db.Column(db.Integer, nullable=False)
	description = db.Column(db.String(255), nullable=False)
	author = db.Column(db.String(255), nullable=False)
	updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
	created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

class Order(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(255), nullable=False)
	card = db.Column(db.Integer, nullable=False)
	name = db.Column(db.String(255), nullable=False)
	updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
	created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
	product_id = db.Column(db.Integer, nullable=False)

@app.route('/admin/pdf/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
	# productのidに一致するデータを受け取る
	product = Product.query.filter_by(id=id).first()
	if request.method == 'GET':
		return render_template('/admin/delete.html', product=product)
	elif request.method == 'POST':
		# productのidに一致するデータを削除する
		db.session.query(Product).filter(Product.id == id).delete()
		# 変更を確定する
		db.session.commit()
		#変更を確定したらpdfに飛ばす
		return redirect(url_for('pdf'))



@app.route('/admin/pdf/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):

	product = Product.query.filter_by(id=id).first()

	if request.method == 'GET':

		return render_template('/admin/edit.html', product=product)

	if request.method == 'POST':



		if 'title' not in request.form or 'price' not in request.form or 'description' not in request.form or 'author' not in request.form:
			flash('指定されていません')
			return redirect(url_for('index'))



		title = request.form['title']
		price = request.form['price']
		description = request.form['description']
		author = request.form['author']

		product.title = title
		product.price = price
		product.description = description
		product.author = author

		db.session.commit()

		print(title, price, description, author)
		return redirect(url_for('pdf'))



@app.route('/admin/order')
def admin_order():
	orders = Order.query.all()
	koramu = db.session.query(Order, func.sum(Product.price)).join(Order, Order.product_id == Product.id).all()
	print(koramu[0][1])
	total_sales_amount = koramu[0][1]
	return render_template('/admin/order.html',orders=orders,total_sales_amount=total_sales_amount)

@app.route('/admin/pdf')
def pdf():
	products = Product.query.all()
	return render_template('/admin/products.html', products=products)



@app.route('/upload/<int:id>')
def upload(id):
	product = db.session.query(Product).filter_by(id=id).first()
	print(product.path)
	return send_from_directory("./upload", product.path)


@app.route('/order/<int:id>', methods=['GET', 'POST'])
def order(id):

	product = db.session.query(Product).filter_by(id=id).first()
	# クライアントがサーバーにしてほしいことを依頼がGETの時
	if request.method == 'GET':



		return render_template('order/order.html', product=product)

	else:
		name = request.form['name']
		email = request.form['email']
		card = request.form['card']

		print(name, email, card)

		new_order = Order(name=name, email=email, card=card, product_id=id)
		db.session.add(new_order)
		db.session.commit()


		return render_template('order/ordercomplete.html', id=id)




@app.route('/products/<int:id>')
def product(id):
	product = db.session.query(Product).filter_by(id=id).first()

	if product:
		print(product.title, product.price, product.author, product.description, product.created_at, product.updated_at)
		return render_template('product/product.html', product=product)
	else:
		return '404ページ無いでーす無いところにアクセスしたバツとしてgta5下さい'
@app.route('/products')
def products():
	# データベースに保存された全てのproductのデータのリスト
	products = Product.query.all()
	print(products)
	return render_template('syouhin.html', products=products)


@app.route('/')
def index():
	# Topページ(index.html)を表示する
	return render_template('index.html')

@app.route('/admin/pdf/upload', methods=['GET', 'POST'])
def upload_pdf():
	if request.method == 'GET':
		return render_template('admin/upload.html')
	else:
		# request.form(送信されたファイル)に'title,price,description,author'が含まれてなければトップページに飛ばすぅっぅぅぅぅぅぅ
		if 'title' not in request.form or 'price' not in request.form or 'description' not in request.form or 'author' not in request.form:
			flash('指定していないのでgta5くれや')
			return redirect(url_for('index'))
		# request.file(送信されたファイル)に'file'が含まれてなければトップページに飛ばすぅっぅぅぅぅぅぅ
		if 'file' not in request.files:
			flash('ファイル指定してないからgta5頂戴')
			return redirect(url_for('index'))


		title = request.form['title']
		price = request.form['price']
		description = request.form['description']
		author = request.form['author']
		file = request.files['file']
		print(title, price, description, author, file)

		filename = secure_filename(file.filename)

		file.save(os.path.join(app.config['UPLOAD_DIR'], filename))

		new_file = Product(title=title, path=filename, price=price, description=description, author=author)
		db.session.add(new_file)
		db.session.commit()

		return "gta5くれや"








if __name__ == '__main__':
	app.run(debug=True)
