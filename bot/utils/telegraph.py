from string import Template
from telegraph.aio import Telegraph


class CreateTelegraph:

    async def create_page(requests, article):
        telegraph = Telegraph()
        print(await telegraph.create_account(short_name='1337'))

        with open('bot/utils/telegraph.html', 'r') as file:
            html_content = file.read()

        url = f'https://www.wildberries.ru/catalog/{article}/detail.aspx'
        rows = ""
        for row in requests:
            page_url = f"https://www.wildberries.ru/catalog/0/search.aspx?page={list(row.values())[0][0]}&sort=popular&search={list(row.keys())[0].replace(' ', '+')}"
            rows += f'<tr><td width="600">{list(row.keys())[0]}</td><td><a href="{page_url}">{list(row.values())[0][0]}-{list(row.values())[0][1]}</a></td><td>0</td><td>{list(row.values())[0][2]}</td><td>{list(row.values())[0][3]}</td></tr>'
        html_content = Template(html_content).substitute(url=url, article=article, rows=rows)
        #.replace('{', '{{').replace('}', '}}').replace('{url}', '{{url}}').replace('{article}', '{{article}}').replace('{rows}', '{{rows}}')
        with open('test.html', 'w') as file:
            file.write(html_content)
        #response = await telegraph.create_page(
        #    'Search',
        #    html_content=html_content,
        #)
        #print(response['url'])

        """<tr>
            <td width="600">поисковый запрос может быть длинным</td>
            <td>1</td>
            <td>1</td>
            <td>1</td>
            <td>1</td>
        </tr>
        <tr>
            <td width="600">поисковый запрос может быть длинным</td>
            <td>2</td>
            <td>2</td>
            <td>2</td>
            <td>2</td>
        </tr>"""