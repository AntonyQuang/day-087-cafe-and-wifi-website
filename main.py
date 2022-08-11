from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)


app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
db = SQLAlchemy(app)
Bootstrap(app)

all_cafes = []
# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Cafe and Wifi Website.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        dictionary = {}

        for column in self.__table__.columns:
            dictionary[column.name] = getattr(self, column.name)
        return dictionary



class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField('Cafe Location on Google Maps (URL)', validators=[DataRequired(), URL()])
    open = StringField('Opening Time (E.g. 8AM)', validators=[DataRequired()])
    close = StringField('Closing Time (E.g. 11:30PM)', validators=[DataRequired()])
    coffee = SelectField('Coffee Rating', choices=["☕", "☕☕", "☕☕☕", "☕☕☕", "☕☕☕☕", "☕☕☕☕☕"], validators=[DataRequired()])
    wifi = SelectField('Wifi Rating', choices=["✘", "💪", "💪💪", "💪💪💪", "💪💪💪", "💪💪💪💪", "💪💪💪💪💪"], validators=[DataRequired()])
    power = SelectField('Wifi Rating', choices=["✘", "🔌", "🔌🔌", "🔌🔌🔌", "🔌🔌🔌", "🔌🔌🔌🔌", "🔌🔌🔌🔌🔌"], validators=[DataRequired()])
    submit = SubmitField('Submit')


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    new_cafe = Cafe(
        name=request.form.get("name"),
        map_url=request.form.get("map_url"),
        img_url=request.form.get("img_url"),
        location=request.form.get("loc"),
        has_sockets=bool(request.form.get("sockets")),
        has_toilet=bool(request.form.get("toilet")),
        has_wifi=bool(request.form.get("wifi")),
        can_take_calls=bool(request.form.get("calls")),
        seats=request.form.get("seats"),
        coffee_price=request.form.get("coffee_price"),
    )
    db.session.add(new_cafe)
    db.session.commit()
    return render_template('add.html', form=new_cafe)


@app.route('/cafes')
def cafes():
    all_cafes = db.session.query(Cafe).all()
    cafes = [cafe.to_dict() for cafe in all_cafes]
    return render_template('cafes.html', cafes=cafes)


if __name__ == '__main__':
    app.run(debug=True)
