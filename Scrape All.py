#Import packages
from pymongo import MongoClient
import snscrape.modules.twitter as sntwitter
from datetime import datetime

# create connection to Mongo DB
client = MongoClient()
db = client['GreenEnergy&Efficiencies_']

#Get Timestamp
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
print("Current Time =", current_time)


# Create lists for years and topics to be scraped
year_list = ['2011','2013','2015','2017','2019','2021']
topic_list = ['Natural Gas','Electric Vehicles','Clean Energy','Renewables', 'Solar Panels', 'Geothermal', 'Energy Rebates', 'Hydro Electricity', 'Coal Power']

# Use snscrape's TwitterSearchScraper to pull tweets
for t in topic_list:     
    for y in year_list:
        parameters = t + ' since:' + y + '-01-01 until:' + y + '-12-31'
        for i,tweet in enumerate(sntwitter.TwitterSearchScraper(parameters).get_items()):
            if i>100000:
                break
            #print(tweet)
            db[t].insert_one({'Datetime': tweet.date, 'Text': tweet.content, 'Likes': tweet.likeCount, 'location':tweet.user.location, 'user':tweet.user.username})






