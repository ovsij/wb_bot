import logging

def get_difference(article : str, today, yesterday):
    if all(article not in today.search_1, article not in today.search_2, article not in today.search_3) \
          or all(article not in yesterday.search_1, article not in yesterday.search_2, article not in yesterday.search_3):
        return ''
    today_page = 1 if article in today.search_1 else 2 if article in today.search_2 else 3
    today_index = today.search_1.index(article) + 1 if today_page == 1 else today.search_2.index(article) + 1 if today_page == 2 else today.search_3.index(article) + 1

    yesterday_page = 1 if article in yesterday.search_1 else 2 if article in yesterday.search_2 else 3
    yesterday_index = yesterday.search_1.index(article) + 1 if yesterday_page == 1 else yesterday.search_2.index(article) + 1 if yesterday_page == 2 else yesterday.search_3.index(article) + 1

    #logging.info(f'today_page {today_page}')
    #logging.info(f'today_index {today_index}')
    #logging.info(f'yesterday_page {yesterday_page}')
    #logging.info(f'yesterday_index {yesterday_index}')
    if today_page == yesterday_page:
        diff = yesterday_index - today_index
    if today_page == 1 and yesterday_page == 2:
        diff = yesterday_index + (100 - today_index)
    if today_page == 1 and yesterday_page == 3:
        diff = yesterday_page + 100 + (100 - today_index)
    if today_page == 2 and yesterday_page == 1:
        diff == -(today_index + (100 - today_index))
    if today_page == 3 and yesterday_page == 1:
        diff == -(today_index + 100 + (100 - today_index))
    if today_page == 2 and yesterday_page == 3:
        diff = -(today_index + (100 - today_index))
    if today_page == 3 and yesterday_page == 2:
        diff = yesterday_index + (100 - today_index)

    if diff > 0:
        return f' (⬆ +{diff})'
    elif diff < 0:
        return f' (⬇ {diff})'
    else:
        return ''