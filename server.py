from flask import Flask, render_template, redirect, flash, request, session
from melons import get_all, get_by_id
from forms import LoginForm
import jinja2
import customers

app = Flask(__name__)
app.secret_key = 'dev'
app.jinja_env.undefined = jinja2.StrictUndefined 

@app.route('/')
def homepage():

    return render_template('base.html')

@app.route("/melons")
def melons():

    melon_list = get_all() # Gets all melons and attributes 
    return render_template("melons.html", melons = melon_list)

@app.route('/melons/<melon_id>')
def melon_details(melon_id):

    my_melon = get_by_id(melon_id) # gets the melon attributes with melon id
    return render_template('melon.html', melon = my_melon)


@app.route("/cart")
def cart():

    if 'username' not in session: # sends user to login form is the user is not logged in
        return redirect("/login")
    
    order_total = 0
    cart_melons = []
    cart = session.get("cart", {}) # Gets the sessions cart

    for melon_id, quantity in cart.items(): # Iterate through the cart, find the attributes of eat melon with the melon id
        melon = get_by_id(melon_id) # accesses melon attributes with melon id

        total_cost = quantity * melon.price # Calculate total cost for this type of melon and add to order total
        order_total += total_cost

        melon.quantity = quantity # Add the quantity and total cost as attributes on the Melon object
        melon.total_cost = total_cost

        cart_melons.append(melon)

    return render_template("cart.html", cart_melons=cart_melons, order_total=order_total)


@app.route("/add_to_cart/<melon_id>")
def add_to_cart(melon_id):

    if 'username' not in session: # Sends user to the login form if user is not logged in
        return redirect("/login")
    
    if 'cart' not in session: # Makes a cart if there is no cart
        session['cart'] = {}

    cart = session['cart'] # Access the cart variable 
    cart[melon_id] = cart.get(melon_id, 0) + 1 # Adds melon id to the cart in incremends its quantity
    session.modified = True 

    flash(f"Melon {melon_id} successfully added to cart.") # Flash message

    return redirect("/cart") # Loads cart display


@app.route("/empty-cart")
def empty_cart():

    session["cart"] = {} # Empties the session cart
    return redirect("/cart")


@app.route("/login", methods=["GET", "POST"])
def login():

    form = LoginForm(request.form)

    if form.validate_on_submit():    # Form has been submitted with valid data
        username = form.username.data
        password = form.password.data

        user = customers.get_by_username(username) # Gets user from customers

        if not user or user['password'] != password: # checks if user exists or if passwords match
            flash("Invalid username or password")
            return redirect('/login')

        session["username"] = user['username'] # Store username in session to keep track of logged in user
        flash("Logged in.")
        return redirect("/melons")

    return render_template("login.html", form=form) # Form has not been submitted or data was not valid
        

@app.route("/logout")
def logout(): # logs user out
   
   del session["username"] # deletes the username cookie
   flash("Logged out.")
   return redirect("/login") 


@app.errorhandler(404)
def error_404(e): # Custom 404 page
   
   return render_template("404.html") 


if __name__ == "__main__":
    app.env = "development"
    app.run(debug=True, port=8000, host="localhost")
