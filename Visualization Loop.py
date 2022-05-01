#Set collection list
topic_list = ['Natural Gas','Electric Vehicles','Clean Energy','Renewables', 'Solar Panels', 'Geothermal', 'Energy Rebates', 'Hydro Electricity', 'Coal Power']
#Iterate through topic list
for t in topic_list:
    import pandas as pd
    from pymongo import MongoClient
    # create connection 
    client = MongoClient()
    db = client['GreenEnergy&Efficiency_Sentiments']
    tickets = db[t]
    results=tickets.find()
    #Create dataframe from collection
    df=pd.DataFrame(data=results)
    #Group by year and find mean sentiment for new dataframe
    df['year'] = pd.DatetimeIndex(df['Datetime']).year
    year_df=df.groupby('year').mean('composite_sentiment')
    year_df=year_df.reset_index(drop=False)
    year_df=year_df.rename(columns={'year': 'Year', 'composite_sentiment': 'Avg. Sentiment'})
    #Create figure based on yearly average sentiment
    import plotly.express as px
    fig = px.bar(year_df, x='Year', y='Avg. Sentiment', title = t+' Sentiments')
    import os
    #Send visualizations to files as pdf and png
    base_dir1=r'C:\Users\Schry\Documents\MSDS696\Visualizations\PDF' 
    base_dir2=r'C:\Users\Schry\Documents\MSDS696\Visualizations\PNG' 
    filename1= t + '.pdf'
    filename2= t + '.png'
    path1= os.path.join(base_dir1, filename1)
    path2= os.path.join(base_dir2, filename2)
    fig.write_image(path1)
    fig.write_image(path2)
    print(t + ' complete')

