import json
import requests
import tweepy
import time

url = 'https://www.cvs.com/immunizations/covid-19-vaccine.vaccine-status.NJ.json?vaccineinfo'
#tweepy credentials
CONSUMER_KEY = "XXXXXX"
CONSUMER_SECRET = "XXXXXX"
ACCESS_KEY = "XXXXXX"
ACCESS_SECRET = "XXXXXX"

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

global numberOfLocations
cities = []
availability = []
availablePlaces = []
def findAppointments():
    global numberOfLocations
    headers = {
        'authority': 'www.cvs.com',
        'method': 'GET',
        'path': '/immunizations/covid-19-vaccine.vaccine-status.NJ.json?vaccineinfo',
        'scheme': 'https',
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'cookie': 'QuantumMetricSessionLink=https://cvs.quantummetric.com/#/users/search?autoreplay=true&qmsessioncookie=607770033e20c5ce6dd3933a0976dbf6&ts=1619161834-1619248234; adh_ps_pickup=on; sab_displayads=on; echome_lean6=off-p0; flipp2=on; mc_videovisit=on; pivotal_forgot_password=off-p0; pivotal_sso=off-p0; ps=on; rxm=on; s2c_akamaidigitizecoupon=on; s2c_digitizecoupon=on; s2c_dmenrollment=off-p0; s2c_herotimer=off-p0; s2c_papercoupon=on; s2c_persistEcCookie=on; s2c_smsenrollment=on; sftg=on; show_exception_status=on; _group1=quantum; gbi_visitorId=cklsg2qe100013b7rnaebuj8f; s2c_newcard=off-p0; aat1=on; DG_SID=71.58.41.187:bfjRDT4ZEhAoOg7pbdo1GXpUD+3vT5Xte2emIaW+2DM; mt.v=2.1425621718.1615008139688; _4c_mc_=999a943d-cee0-4e81-9ae4-691e50bf4a29; QuantumMetricUserID=bc337c167fb128747dab3ed0ea29842e; _gcl_au=1.1.1929245604.1615008206; DG_IID=B1CC3873-DEAE-3BEF-8CA5-6941E647DDC3; DG_UID=3A52AA90-DD22-3E29-AE50-C9C2FCE3C7A8; DG_ZID=C65FEC20-30E0-38A8-A919-9EC2EE7A3E74; DG_ZUID=DCFC427D-960A-354B-8425-82190A363362; DG_HID=F73BC3DB-E53B-3899-BA35-D4CC770D746E; mc_home_new=on; mc_ui_ssr=off-p0; echomeln6=on; mp_cvs_mixpanel=%7B%22distinct_id%22%3A%20%221785356baab7ea-01c28e93f6052e-5771031-240000-1785356baacd3a%22%2C%22bc_persist_updated%22%3A%201617844907782%7D; s2c_securecard=off-p0; pe=p1; acctdel_v1=on; adh_new_ps=on; adh_ps_refill=on; buynow=off; dashboard_v1=off; db-show-allrx=on; disable-app-dynamics=on; dpp_cdc=off; dpp_drug_dir=off; dpp_sft=off; getcust_elastic=on; enable_imz=on; enable_imz_cvd=on; enable_imz_reschedule_instore=on; enable_imz_reschedule_clinic=on; gbi_cvs_coupons=true; ice-phr-offer=off; v3redirecton=false; mc_cloud_service=on; mc_hl7=on; pauth_v1=off; rxdanshownba=off; rxdfixie=on; rxd_bnr=on; rxd_dot_bnr=on; rxdpromo=on; rxduan=on; rxlitelob=off; rxm_phone_dob=on; rxm_demo_hide_LN=off; rxm_phdob_hide_LN=on; rxm_rx_challenge=off; s2c_beautyclub=on; s2c_rewardstrackerbctile=on; s2c_rewardstrackerbctenpercent=on; s2c_rewardstrackerqebtile=on; s2c_rewardstrackerbcpilotue=off; s2cHero_lean6=on; sft_mfr_new=on; v2-dash-redirection=on; ak_bmsc=B9CC4C5DA5C5D3FC989F7F2DF91B3BDF1726AA1C1A720000A81B8360B8EE9923~pl82J3dh3TdEmscMADrwf/WcWq8bS8u6jQBsEzp8AJlR4PtWu8BXoVC8r7c6hHBHBhZtWpo6dhAIUY+36iQhZenp7niip5VpaG5AzuRdqO2epLHy1F1xIYwgj/DbMlwxN9kmVwxgWbFKqSPJ8b8NNGVr6DVNMshof6iU3YPGuHNR9KxKxViefYpmj4eSfmkUbtiXPY0PSXWkN7M8kPG/x5pBM1gqjJPPsN/aW6/qKLeaE=; bm_sz=B8538D8914BE405891F55E3A9BBB5D27~YAAQHKomFyyRw9x4AQAAgwgkAAu0cLHRmInYFmhonGH3n1CXd49JEpUH+DyM7OkK62gR92TdZ4jteDbE4rykNtvHdYX1IAv8jmXdb+ofsfCiSYjHzu0hZpOWTmUzecQK1rK8AxJf//rdTDWton0dHOCM3t+UEPF6Znn6Tqa7/tDPKa87X8+2UB5VKuA=; AMCVS_06660D1556E030D17F000101%40AdobeOrg=1; AMCV_06660D1556E030D17F000101%40AdobeOrg=-330454231%7CMCIDTS%7C18741%7CMCMID%7C61727826069222442583631668589362072650%7CMCAAMLH-1619809832%7C7%7CMCAAMB-1619809832%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1619212232s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C3.1.2; mt.sc=%7B%22i%22%3A1619205032542%2C%22d%22%3A%5B%5D%7D; gpv_p10=www.cvs.com%2Fimmunizations%2Fcovid-19-vaccine; s_cc=true; QuantumMetricSessionID=607770033e20c5ce6dd3933a0976dbf6; gbi_sessionId=cknuovccy00003b9dl91o5kpp; _abck=7FAACFFF52295658AFFB21A1CFF8DBBC~0~YAAQHKomF4GRw9x4AQAAPxEkAAWwOgpSsD3lSbTKI9i2Bq30Q0vkDGw+GgdzkdlioeJdn8ZIKQM/P9cVuW03pGdFAB5KYlNq3ACR0lRTkK17oF/OoeIss46BFOhbBIynLkRM3XooY+7rRAGI0mvc/Zm/8k5QSvxMWzW3+RdxXNpamjI8w58H9OxrHUxaELuuSGeJ4PXJe2F9ORuPWZn0oEIKqz4kQWDMH8Y3Rte4hV+taWS3v0va8bpu1ByPJf+W+n1846ubkkE50zT0lhkMpvreeXkgvSlJqioMFsGoSUp4V+32H+rO2/FCsV0ckfn7yxz3Thq3B0+ISUt087Ob+9VWdEUQhg3XzYb3w7jZnbDzPiaQJtQsyWFQ4csmKIJrxoH7AQeRGdIw3KOJmFpl18YFWlWm~-1~||-1||~-1; akavpau_www_cvs_com_general=1619205643~id=c9d4c215350df2f63320b9aac6d2fa39; utag_main=v_id:0178af118262003b7a11f7274ff003073003206b00c9e$_sn:4$_ss:0$_st:1619207023243$vapi_domain:cvs.com$_pn:2%3Bexp-session$ses_id:1619205032185%3Bexp-session; CVPF=3guo_UCstm0SzLCuoXdEu8X2tdu59R5-kOvbMn1BKmxJxG0yZGgJJkw; gpv_e5=cvs%7Cdweb%7Cimmunizations%7Ccovid-19-vaccine%7Ccovid%20vaccine%20%28covid-19%20immunization%20updates%29%20%7C%20cvs%20pharmacy; bm_sv=820FC74AE660980FAEC23D42BAB65930~rEi0OxbAhRno6sLaYvNaG4NBOJuBL+ZOTa2UqIsfrsPMH9/ch4pOpcGdZH4Baqgj9vEbI/N//qRg7jltmCnYGASnLKhv6drYEOK+AF1aaR9tgHFnIinNSIiPT42oZXE+DeJhlLHSuICjXdTYIpT7WQ==; RT="z=1&dm=cvs.com&si=29c89e49-d6a6-484c-b406-3989d08b77d1&ss=knuovap2&sl=4&tt=88e&bcn=%2F%2F173c5b04.akstat.io%2F&ld=4872"; s_sq=cvshealthretailprod%3D%2526c.%2526a.%2526activitymap.%2526page%253Dcvs%25257Cdweb%25257Cimmunizations%25257Ccovid-19-vaccine%25257Ccovid%252520vaccine%252520%252528covid-19%252520immunization%252520updates%252529%252520%25257C%252520cvs%252520pharmacy%2526link%253DGet%252520started%2526region%253Dstateform%2526pageIDType%253D1%2526.activitymap%2526.a%2526.c',
        'pragma': 'no-cache',
        'referer': 'https://www.cvs.com/immunizations/covid-19-vaccine',
        'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
    }
    body = {'vaccineinfo':""}
    r = requests.get(url = url, data = json.dumps(body), headers = headers)
    jsonData = r.json()

    # we grab the json data, parse for the data we actually care about, then append those to the cities and availability lists
    for i in jsonData['responsePayloadData']['data']['NJ']:
        cities.append(i['city'].capitalize())
        availability.append(i['status'])
    # we create a dictionary out of the two lists
    dictionary = {k: v for k, v in zip(cities, availability)}
    # if "Available" is a value for any key, append it to the list of availablePlaces
    if len(dictionary) != 0:
        for k,v in dictionary.items():
            if v == "Available":
                availablePlaces.append(k)
        else:
            pass
    else:
        print("Looks like theres a bit of a bug...")

def tweet():
    temp = []
    try:
        # Below we grab the last tweet the robot has tweeted to make sure we try not to send duplicate tweets.
        for status in tweepy.Cursor(api.user_timeline, tweet_mode = "extended").items(limit = 1):
            temp.append(status.full_text)
        # Below we build the tweet. "Found X CVS location(s) with appointments: Long Branch, Red Bank, Freehold"
        message = "Found " + str(len(availablePlaces)) + " CVS location(s) with appointments: \n" + "\n" + ", ".join(availablePlaces)
        split = temp[0].split("http")
        sub = split[0].rstrip()
        print("--------------------------------------------------------------")
        if sub != message: #If the previous tweet != to the current tweet we're trying to send
            if len(message) <= 280: # if the tweet meets the character requirements
                print("Tweets are unique and less than 280 characters\n")
                print("Attempting to post tweet...")
                api.update_status(
                    "Found " + str(len(availablePlaces)) + " CVS location(s) with appointments: \n" + "\n" + ", ".join(availablePlaces) + "\n https://rb.gy/vv4wof")
                print("\nTweet has been posted successfully!")
            if len(message) > 280: # if the tweet we're trying to send is longer than 280 char's, send a generic tweet!
                print("This tweet is longer than 280 characters. Sending a generic tweet instead.")
                api.update_status("Found " + str(len(availablePlaces)) + " CVS location(s) with appointments.\n\nUnfortunately, the list of available locations is too long to tweet out. Please check CVS' website for locations near you.\n \n https://rb.gy/vv4wof")
                print("Generic Tweet successfully posted.")
        else:
            print("\n-----------------------------------\n")
            print("They're the same")
            print("Found " + str(len(availablePlaces)) + " CVS location(s) with appointments: \n" + "\n" + ", ".join(
                availablePlaces) + "\n https://rb.gy/vv4wof")
    #
    except tweepy.TweepError as e:
        if e == "[{'code': 187, 'message': 'Status is a duplicate.'}]":
            print("Failed to post tweet. Tweet was a duplicate.")
            return
        else:
            print("Error! Take a look: ")
            print(e)
            return

while True:
    del availablePlaces[:]
    findAppointments()
    if not availablePlaces:
        print("No available appointments, we will check again after 60 seconds\n")
        time.sleep(60)
    else:
        if len(availablePlaces) > 0:
            tweet()
            print("sleeping for 60 seconds")
            time.sleep(60)