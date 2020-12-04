'''Cupcake App API'''
from flask import Flask, request, jsonify,render_template
from models import db, connect_db, Cupcake
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "oh-so-secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS']= False
debug = DebugToolbarExtension(app)

connect_db(app)
# db.create_all()

# GET /api/cupcakes
# Get data about all cupcakes.
# Respond with JSON like: {cupcakes: [{id, flavor, size, rating, image}, ...]}.
# The values should come from each cupcake instance.
@app.route('/api/cupcakes')
def list_all_cupcakes():
    '''Return JSON {cupcakes: [{id, flavor, size, rating, image}, ...]}'''
    cupcakes = Cupcake.query.all()
    seralized = [cupcake.serialize() for cupcake in cupcakes]
    return jsonify(cupcakes=seralized)

# GET /api/cupcakes/[cupcake-id]
# Get data about a single cupcake.
# Respond with JSON like: {cupcake: {id, flavor, size, rating, image}}.
# This should raise a 404 if the cupcake cannot be found.
@app.route('/api/cupcakes/<cupcake_id>')
def list_single_cupcake(cupcake_id):
    '''Return JSON {cupcake: {id, flavor, size, rating, image}}.'''
    cupcake = Cupcake.query.get(cupcake_id)
    seralized = cupcake.serialize()
    return jsonify(cupcake=seralized)


# POST /api/cupcakes
# Create a cupcake with flavor, size, rating and image data from the body of the request.
# Respond with JSON like: {cupcake: {id, flavor, size, rating, image}}.
@app.route('/api/cupcakes', methods =["POST"])
def create_cupcake():
    '''Return JSON {cupcake: {id, flavor, size, rating, image}}.'''
    flavor = request.json['flavor']
    size = request.json['size']
    rating = request.json['rating']
    image = request.json['image']

    new_cupcake = Cupcake(flavor=flavor, size=size,rating=rating, image=image)
    
    db.session.add(new_cupcake)
    db.session.commit()

    seralized = new_cupcake.serialize()
    return (jsonify(cupcake=seralized),201)

# PATCH /api/cupcakes/[cupcake-id]
# Update a cupcake with the id passed in the URL and flavor, size, rating and image data from the body of the request. You can always assume that the entire cupcake object will be passed to the backend.
# This should raise a 404 if the cupcake cannot be found.
# Respond with JSON of the newly-updated cupcake, like this: {cupcake: {id, flavor, size, rating, image}}.
@app.route('/api/cupcakes/<cupcake_id>', methods=['PATCH'])
def update_cupcake(cupcake_id):
    '''Updates a given cupcake and respons with JSON of that updated todo'''
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    cupcake.flavor = request.json.get("flavor", cupcake.flavor)
    cupcake.size = request.json.get("size", cupcake.size)
    cupcake.rating = request.json.get("rating", cupcake.rating)
    cupcake.image = request.json.get("image", cupcake.image)
    db.session.commit()
    return jsonify(cupcake=cupcake.serialize())


# DELETE /api/cupcakes/[cupcake-id]
# This should raise a 404 if the cupcake cannot be found.
# Delete cupcake with the id passed in the URL. Respond with JSON like {message: "Deleted"}.
@app.route('/api/cupcakes/<cupcake_id>',methods=['DELETE'])
def delete_cupcake(cupcake_id):
    '''Deletes a given cupcake'''
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message='Deleted')

@app.route('/')
def index_view():
    return render_template('index.html')