from datetime import datetime, date


def make_date(date_range_str):
    start = date.today()
    end = datetime.strptime(date_range_str, '%m/%d/%Y').date()
    return start, end


def return_book_operation(data):
    data['rent_obj'].return_date = data['return_date']
    data['rent_obj'].penalty = data['penalty']
    data['rent_obj'].actual_cost = data['cost']
    data['rent_obj'].save(update_fields=['return_date', 'penalty', 'actual_cost'])

    data['product'].durability = data['product'].durability + data['durability_add']
    if data['product'].type == 'meter':
        data['product'].mileage = data['product'].mileage - data['mileage_loss']
    data['product'].needing_repair = data['needing_repair']
    data['product'].availability = True
    data['product'].save()