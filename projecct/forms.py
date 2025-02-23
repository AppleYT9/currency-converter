from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SubmitField
from wtforms.validators import DataRequired, Length

class CurrencyForm(FlaskForm):
    from_currency = StringField("From Currency (e.g., USD)", validators=[DataRequired(), Length(min=3, max=3)])
    to_currency = StringField("To Currency (e.g., INR)", validators=[DataRequired(), Length(min=3, max=3)])
    amount = DecimalField("Amount", validators=[DataRequired()])
    submit = SubmitField("Convert")