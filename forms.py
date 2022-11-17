from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField
from wtforms.validators import InputRequired
from datetime import date


class SearchForm(FlaskForm):
    search = StringField(label="Stock Ticker",
                         validators=[InputRequired()],
                         description="e.g. GOOGL or GOOGL,AAPL"
                         )
    date_from = DateField(label="Date From", format="%Y-%m-%d", default=date.today())
    date_to = DateField(label="Date To", format="%Y-%m-%d", default=date.today())
    submit = SubmitField(label="Search")
