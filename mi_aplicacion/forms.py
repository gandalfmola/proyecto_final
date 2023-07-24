from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Length



class MovementForm(FlaskForm):
    moneda_from = SelectField("From", validators=[DataRequired("Campo obligatorio")], choices=["EUR", "BTC", "ETH", "ADA", "XRP", "LTC", "BNB", "USDT", "SOL", "MATIC"])
    moneda_to = SelectField("From", validators=[DataRequired("Campo obligatorio")], choices=["EUR", "BTC", "ETH", "ADA", "XRP", "LTC", "BNB", "USDT", "SOL", "MATIC"])
    cantidad = FloatField("Cantidad", validators=[DataRequired("Este campo es obligatorio")])

    boton_calcular = SubmitField("Calcular")
    boton_comprar = SubmitField("Comprar")

    hid1 = HiddenField()
    hid2 = HiddenField()
    hid3 = HiddenField()