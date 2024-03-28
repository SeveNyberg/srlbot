import requests
import time
import datetime
from srlbot_plugins import R_index, timestamp, post, read
from authkey import token


# Channel id for bot-test
channel_bot_test = "nunmku933pbntxio81uy8hfmwy"
# Channel id for aurora-watch
channel_aurora = "c9aysk4bc3be9cb3m6wncgokyc"

post(channel_bot_test, f"Hello! Boot timestamp: {timestamp()}")


def main():
    
    print("Bot booted.")
    t_prev_msg = 0
    t_prev_msrt = 1
       
    while(True):
        
        # Have loop check everything every second instead of as fast as possible to conserve the machine
        time.sleep(1)
        
        # R-index checking and conditional posting
        if time.time() - t_prev_msrt > 299:
            
            #Fetch data
            try:
                R = R_index()
            except:
                print("Problem at R-index at", timestamp())
        
            # For post testing
            #R = 130

            if R > 125 and time.time()-t_prev_msg > 7200:

                message =  f"Current  R-index at Nurmijärvi ({R:.2f}) exceeds the threshold! (https://en.ilmatieteenlaitos.fi/auroras-and-space-weather)"
                # For post testing
                #message = "Testing...""
                
                try:
                    post(channel_aurora, message)
                    t_prev_msg = time.time()
                except:
                    print("Problem at aurora post at", timestamp())
                
        response = read(channel_bot_test)
        
        if response == "--help":
            post(channel_bot_test, "--help for help")
            
        if response == "--magact":
            post(channel_bot_test, f"Current R-index at Nurmijärvi: {R:.2f}")
        
        
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Program stopped at", timestamp())
    #except:
       # print("Program stopped at", timestamp())
        #main()
