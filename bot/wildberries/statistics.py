from datetime import datetime, timedelta
import requests

class Statistics:
    def get_reportDetailByPeriod(token):
        url = 'https://statistics-api.wildberries.ru/api/v1/supplier/reportDetailByPeriod'
        datetime_now = datetime.now()
        print(datetime_now)
        params = {'dateFrom': datetime_now - timedelta(days=10), 'dateTo': datetime_now}
        headers = {'Authorization': token}
        response = requests.get(url, params=params, headers=headers)
        #print(response.status)
        if response.status_code == 200:
            return response.json()[0]
        else:
            return False
