from models import Location

def date_format(date):
    meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo',
        'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre',
        'Noviembre', 'Diciembre']
    mes = meses[date.month - 1]
    return "{} de {} del {}".format(date.day, mes, date.year)


def locations():
    return [(g.id, g.name) for g in Location.query.all().order_by('name')]