def date_format(date):
    meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo',
        'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre',
        'Noviembre', 'Diciembre']
    mes = meses[date.month - 1]
    return "{} de {} del {}".format(date.day, mes, date.year)
