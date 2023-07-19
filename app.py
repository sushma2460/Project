from flask import Flask,render_template,url_for,request,redirect
from markupsafe import escape
import mysql.connector

db=mysql.connector.connect(
    host='localhost',
    user='root',
    password='mannava@4598',
    database='tripura'
) 


cur=db.cursor(dictionary=True)

app=Flask(__name__)

@app.route('/home')
def homePage():
    return render_template('home.html')


@app.route('/register')
def registerPage():
    return render_template('register.html')    


@app.route('/customer')
def registerPageee():
    k=[]
    cur.execute("select * from items")
    value=cur.fetchall()
    a=[]
    for j in value:
        print(j)
        dum=[]
        dum.append(j['item'])
        k.append(j['item'])
        dum.append(j['price'])
        a.append(dum)


    return render_template('customer.html',value=a,dd=k,len=len(k))



@app.route('/admin')
def index():
    cur.execute("select * from cust")
    data=cur.fetchall()
    k=[]
    for i in data:
        print(i)
        dummy=[]
        dummy.append(i['name'])
        dummy.append(i['year'])
        dummy.append(i['item'])
        dummy.append(i['quantity'])
        dummy.append(i['price'])
        dummy.append(i['totalprice'])
        k.append(dummy)

    return render_template('admin.html',data=k)

@app.route('/order',methods=['post'])
def formpage1():
    name=request.form['name']
    year=request.form['year']
    item=request.form['item']
    quantity=request.form['quantity']
    print(item,quantity)
    # read data from table
    cur.execute("select * from items")
    data=cur.fetchall()
    for i in data:
        if i['item']==item:
            price=i['price']
    totalprice=int(quantity)*int(price)
    sql="INSERT INTO cust(name,year,item,quantity,price,totalprice) VALUES(%s,%s,%s,%s,%s,%s)"
    values=(name,year,item,quantity,price,totalprice)
    cur.execute(sql,values)
    db.commit()
    return render_template('order.html')


@app.route('/insert',methods=['post'])
def insertpage1():
    item=request.form['item']
    price=request.form['price']
    print(item,price)
    sql="INSERT INTO items(item,price) VALUES(%s,%s)"
    values=(item,price)
    cur.execute(sql,values)
    db.commit()
    return redirect('/admin') 


@app.route('/delete',methods=['post'])
def deletepage1():
    cur.execute('delete from items where item = ?', [request.form['item']])
    db.commit()
    return redirect('/admin') 




@app.route('/login',methods=['post'])
def loginpage2():
    name=request.form['name']
    password=request.form['password']
    sql='select * from loginadm'
    cur.execute(sql)
    result=cur.fetchall()
    data=[]
    for i in result:
        print(i)
        data.append(i)
    j=0
    print(data)
    for i in data:
        if name==i['name'] and password==i['password']:
            p=1
        else:
            p=0
    if p==1:
        return redirect('/admin')
    else:
        return render_template('error.html')        

   
    

if __name__=='__main__':
    app.run(debug=True)
