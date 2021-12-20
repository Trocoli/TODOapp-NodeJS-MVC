from django.core.exceptions import ValidationError

def Validar_Matricula(value):
    if value.isdigit()== True:
        return value
    else:
        raise ValidationError('A matrícula só possui números!')

