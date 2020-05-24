from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, request
	

from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker

from test import Base, Produce, ProduceItem



app = Flask(__name__)



engine = create_engine('sqlite:///producemenuB.db')

Base.metadata.bind = engine



DBSession = sessionmaker(bind=engine)

session = DBSession()


def temp():
	print("This is the temp method!!")
	return ""

@app.route('/produce/<int:produce_id>/menu/JSON')
def produceMenuJSON(produce_id):
	produce = session.query(Produce).filter_by(id=produce_id).one()
	items = session.query(ProduceItem).filter_by(produce_id=produce_id).all()
	return jsonify(ProduceItem=[i.serialize for i in items])

@app.route('/produce/<int:produce_id>/')

def produceMenu(produce_id):
	temp()
	api_address='http://api.openweathermap.org/data/2.5/weather?id=4373238&APPID=924d6ca7c2acd9294d6e042394ead7f4'

	json_data=requests.get(api_address).json()
	test = json_data['main']
	print(json_data)
	print(((json_data['main']['temp'])-273.15)*1.8+32)
	
	produce = session.query(Produce).filter_by(id=produce_id).one()
	
	items = session.query(ProduceItem).filter_by(produce_id=produce.id)	

	return render_template('menu.html', produce = produce, items = items )	
	

@app.route('/produce/<int:produce_id>/new',methods=['GET','POST'])

def newMenuItem(produce_id):
	items = session.query(ProduceItem).all() 
		
	if request.method == 'POST':		
		newItem = ProduceItem(name=request.form['name'],id =request.form['id'], description =request.form['description']\
		,price =request.form['price'],type =request.form['type'],path=request.form['path'],\
		produce_id=produce_id)
		session.add(newItem)
		session.commit()
		flash ("Menu Item added!!")
		return redirect(url_for('produceMenu', produce_id=newItem.produce_id))
	else:
		return render_template('newmenuitem.html',produce_id=produce_id, items=items)

@app.route('/produce/<int:produce_id>/<int:id>/edit',methods=['GET','POST'])

def editMenuItem(produce_id,id):
	editedItem =  session.query(ProduceItem).filter_by(id=id).one()
	if request.method == 'POST':
		if request.form['name']:
			editedItem.name=request.form['name']
			print editedItem.name
		if request.form['id']:
			editedItem.id=request.form['id']
		if request.form['description']:
			editedItem.description=request.form['description']
		if request.form['price']:
			editedItem.price=request.form['price']
		if request.form['type']:
			editedItem.type=request.form['type']
		if request.form['path']:
			editedItem.path=request.form['path']
		if request.form['produce_id']:
			editedItem.produce_id=request.form['produce_id']
		session.add(editedItem)
		session.commit()
		flash ("Menu Item edited!!")
		return redirect(url_for('produceMenu', produce_id=produce_id))
	return render_template('editMenuItem.html',produce_id=produce_id,id=id,editedItem=editedItem)
	#return "This is the editedMenuItem method."
	
@app.route('/produce/<int:produce_id>/<int:id>/delete',methods=['GET','POST'])

def deleteMenuItem(produce_id,id):
	deletedMenuItem = session.query(ProduceItem).filter_by(id=id).one()	
	if request.method=='POST':		
		session.delete(deletedMenuItem)
		session.commit()
		flash ("Menu Item deleted!!")
		return redirect(url_for('produceMenu', produce_id=produce_id))
	else:
		return render_template('deleteMenuItem.html',produce_id=produce_id,id=id,deletedMenuItem=deletedMenuItem)

if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host = '0.0.0.0', port = 9500)