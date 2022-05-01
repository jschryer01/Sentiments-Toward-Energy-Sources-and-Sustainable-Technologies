#Read in collection List
topic_list = ['Natural Gas','Electric Vehicles','Clean Energy','Renewables', 'Solar Panels', 'Geothermal', 'Energy Rebates', 'Hydro Electricity', 'Coal Power']
for t in topic_list:
    print(t)
    #Import pymongo and pandas to read in existing data into a dataframe
    from pymongo import MongoClient
    import pandas as pd
    # create connection to data in pymongo
    client = MongoClient()
    db = client['GreenEnergy&Efficiencies_']
    tickets = db[t]
    results=tickets.find()
    df=pd.DataFrame(data=results)
    df
    
    #Perform initial data cleaning for sentiment analysis purposes
    #Remove digits
    df['clean_text'] = df.Text.str.replace('\d+','')
    #Remove web addresses
    df['clean_text'] = df['clean_text'].apply(lambda x: ' '.join([word for word in x.split() if 'http' not in word  ]))
    #Remove duplicates
    df.drop_duplicates(subset=['clean_text'], keep='first', inplace=True)
    
    #Import vader and perform sentiment analysis
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    sid_analyzer = SentimentIntensityAnalyzer()
    sentiment_dict = df['clean_text']
    analyzer = SentimentIntensityAnalyzer()
    df['composite_sentiment'] = [analyzer.polarity_scores(x)['compound'] for x in df['clean_text']]
    
    #Insert df with newly generated sentiments to a new collection
    db2 = client['GreenEnergy&Efficiency_Sentiments']
    collection = db2[t]
    collection.insert_many(df.to_dict('records'))
    print(t+' Complete')
    
    
    
    