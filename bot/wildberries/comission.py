import pandas as pd

async def create_comission(db_request):
    df = pd.read_csv('bot/wildberries/сomission.csv', sep=';')
    for i in range(len(df)):
        await db_request.create_comission(category=str(df.iloc[i]['category']), 
                                    subject=str(df.iloc[i]['subject']),
                                    percent=str(df.iloc[i]['percent']))
