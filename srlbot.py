 #!/usr/bin/env python3

import time
from srlbot_plugins import R_index, timestamp, post, read
from authkey import token


# Channel IDs for posting and reading different channels, can be found in channel information in Mattermost
from authkey import channel_bot_test
from authkey import channel_aurora

# Set timers for posting magnetic activity and fetching magnetic activity data
t_prev_msg = 0
t_prev_msrt = 1

def main():
    
    global t_prev_msg
    global t_prev_msrt
        
    # Boot post to channel bot-test
    try:
        #post(channel_bot_test, f"Hello! Boot timestamp: {timestamp()}")
        print("Bot booted.")
    except:
        print("Boot unsuccesful.")
    

    # Start main program loop
    while(True):
        
        # Have loop check everything every second instead of as fast as possible to conserve the machine
        time.sleep(1)
        
        # Check R-index every ~5 minutes
        if time.time() - t_prev_msrt > 299:
            
            t_prev_msrt = time.time()
            # Get the R-index 
            try:
                R = R_index()
            except:
                print("Problem at R-index at", timestamp())
                R = 0
        
            # Check if R-index exceeds the set threshold and it has been enough time from last post (~20 h) 
            if R > 120 and time.time()-t_prev_msg > 72000:
                
                # Message format to post 
                message =  f"Current R-index at Nurmijärvi (R = {R:.2f}) exceeds the threshold! (https://en.ilmatieteenlaitos.fi/auroras-and-space-weather)"
                # Post the message and reset the timer
                try:
                    post(channel_aurora, message)
                    t_prev_msg = time.time()
                except:
                    print("Problem at aurora post at", timestamp())
                
                
        # Commands ----------
        # Command for printing all available commands
        help_cmd = "--help"      
        help_msg =  f"""--help for help
--magact for current magnetic activity at Nurmijärvi station"""
        
        # Command for printing current R-index at Nurmijärvi
        magact_cmd = "--magact"
        magact_msg = f"Current R-index at Nurmijärvi: {R:.2f} (https://en.ilmatieteenlaitos.fi/auroras-and-space-weather)"
        
        # Command for freezing bot in case of malfunction
        freeze_cmd = "--freeze"
        freeze_msg = "Bot frozen for 24 hours."
        
        # -------------------
        
        # Read the recently arrived messages in channel bot-test 
        response = read(channel_bot_test)
        # Check if needs responding to
        if response == help_cmd:
            post(channel_bot_test, help_msg)
        if response == magact_cmd:
            post(channel_bot_test, magact_msg)
        if response == freeze_cmd:
            post(channel_bot_test, freeze_msg)
            time.sleep(86400)
            
            
        # Read the recently arrived messages in channel bot-test 
        response = read(channel_aurora)
        # Check if needs responding to
        if response == help_cmd:
            post(channel_aurora, help_msg)
        if response == magact_cmd:
            post(channel_aurora, magact_msg)
            
        
if __name__ == "__main__":

    while True:
        try:
            main()
        # If script runs into an error, try rebooting
        # If script is stopped by hand, stop it 
        except KeyboardInterrupt:
            print("Program stopped at", timestamp())
            break
        except:
            print("Program rebooted at", timestamp())
            continue
                
   