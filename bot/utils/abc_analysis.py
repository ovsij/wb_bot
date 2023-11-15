from datetime import datetime, timedelta

def get_abc(db_request, product_id, seller_id):
    products = db_request.get_product(seller_id=seller_id)
    products_revenue = {}
    total_revenue = 0
    for product_entity in products:
        sales_list = db_request.get_sale(product_id=product_entity.id, type='S', period=f"{(datetime.now() - timedelta(days=91)).strftime('%d.%m.%Y')} - {datetime.now().strftime('%d.%m.%Y')}")
        sales_revenue = sum([s['priceWithDisc'] for s in sales_list])
        products_revenue[product_entity.id] = sales_revenue
        total_revenue += sales_revenue
    sorted_products_revenue = sorted(products_revenue.items(), key=lambda item: item[1], reverse=True)

    cummulative_total = 0
    for product, revenue in sorted_products_revenue:
        abc_percent = revenue / total_revenue * 100
        cummulative_total += abc_percent
        if product == product_id:
            if cummulative_total <= 80:
                abc = 'A'
            elif  cummulative_total <= 95:
                abc = 'B'
            else:
                abc = 'C'
            return abc, round(abc_percent, 2)

