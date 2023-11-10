from string import Template



def create_page(requests, article):

    with open('bot/utils/telegraph.html', 'r') as file:
        html_content = file.read()

    url = f'https://www.wildberries.ru/catalog/{article}/detail.aspx'
    rows = ""
    for row in requests:
        page_url = f"https://www.wildberries.ru/catalog/0/search.aspx?page={list(row.values())[0][0]}&sort=popular&search={list(row.keys())[0].replace(' ', '+')}"
        rows += f'<tr><td width="600">{list(row.keys())[0]}</td><td><a href="{page_url}">{list(row.values())[0][0]}-{list(row.values())[0][1]}</a></td><td>0</td><td>{list(row.values())[0][2]}</td><td>{list(row.values())[0][3]}</td></tr>'
    html_content = Template(html_content).substitute(url=url, article=article, rows=rows)
    with open('test.html', 'w') as file:
        file.write(html_content)
    