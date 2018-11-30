# -*- coding: utf-8 -*-


def date_format(date):
    """Hace un formateo a fecha larga"""
    meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo',
        'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre',
        'Noviembre', 'Diciembre']
    mes = meses[date.month - 1]
    return "{} de {} del {}".format(date.day, mes, date.year)
