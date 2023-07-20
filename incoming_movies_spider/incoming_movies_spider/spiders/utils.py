from datetime import datetime

def clean_date(raw_date : str):
    elements = raw_date[0][1:-1].split(" ")

    months = {
        "janvier": "01",
        "février": "02",
        "mars": "03",
        "avril": "04",
        "mai": "05",
        "juin": "06",
        "juillet": "07",
        "août": "08",
        "septembre": "09",
        "octobre": "10",
        "novembre": "11",
        "décembre": "12"
    }

    elements[1] = months[elements[1]]
    date_str = '-'.join(elements[::-1])
    print(type(date_str))
    date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
    return date_obj

def delete_vues(views : str):
    final = ""
    for v in views:
        if v in '1234567890':
            final+=v
    return int(final)

def clean_views(views):
    final = []
    if type(views) == list:
        for v in views:
            final.append(delete_vues(v))
    else:
        return delete_vues(views)
    if final:
        return max(final)
    else:
        return final