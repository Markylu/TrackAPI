import requests
import json
from pprint import pprint
from datetime import datetime
import pandas as pd
import numpy as np
import schedule
import time

# variables
url = f"https://api.hypixel.net/skyblock/bazaar"
mydict = {32:95}
data = 0
bPrice = 0
sPrice = 0
demand = 0
supply = 0
sum = 0
when = 0
TrackBPrice = []
TrackSPrice = []
Tracktime = []
profitof100 = 0
primeBPrice = 0
primeSPrice = 0
primewhen = 0
tracking = 0
overtime = 0
df = pd.read_csv("/Users/markuslu/HypixelAPI/TrackInvestments/track.csv",index_col=0)

# start inputs
iteminp = input("what item would you like: ")
first = int(input("Is this the inital price? (1 for True or 0 for False): "))

# task functions
def idFormat(org):
      new = org.translate(mydict).upper()
      return new

def getInfo(call):
  r = requests.get(call)
  return r.json()

def setInfo():
      global data, bPrice, sPrice, demand, supply, sum, when
      data = getInfo(url)
      bPrice = data['products'][idFormat(iteminp)]['buy_summary'][0]['pricePerUnit']
      sPrice = data['products'][idFormat(iteminp)]['sell_summary'][0]['pricePerUnit']
      demand = data['products'][idFormat(iteminp)]['quick_status']['sellVolume']
      supply= data['products'][idFormat(iteminp)]['quick_status']['buyVolume']
      sum = data['products'][idFormat(iteminp)]['quick_status']
      when = datetime.now()

def percent(buy,sell):
      try:
            answ = (sell - buy)/buy * 100
      except ZeroDivisionError:
            answ = 0.0
      return answ
def summary():
      print(url)
      pprint("Sell Price: {:,}".format(sPrice))
      pprint("Buy Price: {:,}".format(bPrice))
      pprint("Supply: {:,}".format(supply))
      pprint("Demand: {:,}".format(demand))
      print(f"Time Cheack: {when}")

def primeset():
      global data, primeBPrice, primeSPrice, primeDemand, primeSupply, primesum, primewhen, primedata
      data = getInfo(url)
      primedata = df[(df["prime"] == 1) & (df["item"] == idFormat(iteminp))]
      primeBPrice = primedata.loc[0,"bprice"]
      primeSPrice = primedata.loc[0,"sprice"]
      primewhen = primedata.loc[0,"when"]
      print(primeBPrice)
      print(type(primeBPrice))


def track():
      global profitof100, tracking, df
      tracking = pd.DataFrame(np.array([[bPrice, sPrice, idFormat(iteminp),first,when]]), columns=['bprice', 'sprice', 'item','prime','when'])
      df = df.append(tracking)
      df.to_csv("/Users/markuslu/HypixelAPI/TrackInvestments/track.csv")
      profitof100 = percent(primeBPrice, sPrice)

def settrack():
      setInfo()
      track()
      print("close the program to stop tracking.")
      print("You have {}% profit".format(profitof100))
            
def main():
      global first, overtime, overint
      setInfo()
      if first == 1:
            summary()
            print(idFormat(iteminp))
            track()
            first = 0
            print(df.head)
      else:
            summary()
            print(idFormat(iteminp))
            primeset()
            track()
            print("You have {}% profit".format(profitof100))
            print(df.head)
      if int(input("Would you like to track (1) or not track(2)")) == 1:
            overint = int(input("Every what minute would you like to cheack?(recommended 15 - 30) "))
            overtime = True
      else:
            overtime = False

      schedule.every(overint).minutes.do(settrack)

      while overtime == True:
            schedule.run_pending()
            time.sleep(1)

main()
