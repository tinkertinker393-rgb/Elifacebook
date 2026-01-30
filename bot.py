import time
import random
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

def setup_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    # Masking the bot as a real human browser
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36")
    return webdriver.Chrome(options=options)

def live_monitor():
    driver = setup_driver()
    wait = WebDriverWait(driver, 25)
    
    try:
        # 1. Login once
        print("🔑 Logging into Facebook...")
        driver.get("https://www.facebook.com")
        wait.until(EC.presence_of_element_located((By.ID, "email"))).send_keys("0746404008")
        driver.find_element(By.ID, "pass").send_keys("val8525" + Keys.RETURN)
        time.sleep(12) # Let the homepage fully settle

        print("🚀 Monitoring for immediate updates...")

        while True:
            # --- ACTION A: CHECK NEWEST STORIES ---
            try:
                # Find the first story in the tray
                story_tray = driver.find_element(By.XPATH, "//div[@aria-label='Stories']//div[@role='link']")
                story_tray.click()
                print("👀 Checking latest stories...")
                
                for _ in range(6): # Check up to 6 new stories
                    time.sleep(random.uniform(6, 11))
                    try:
                        # Attempt to 'Heart' the story
                        heart = driver.find_element(By.XPATH, "//div[@aria-label='Like' or @aria-label='React']")
                        heart.click()
                        print("❤️ Reacted to a story.")
                    except: pass
                    # Go to next story immediately
                    ActionChains(driver).send_keys(Keys.ARROW_RIGHT).perform()
                
                # Close viewer to return to feed
                ActionChains(driver).send_keys(Keys.ESCAPE).perform()
            except:
                print("ℹ️ No new stories found right now.")

            # --- ACTION B: CHECK NEWEST POSTS ---
            print("🔄 Refreshing feed for new posts...")
            driver.get("https://www.facebook.com/?sk=h_chr") # This force-sorts by 'Most Recent'
            time.sleep(6)

            # Find 'Like' buttons for the top newest posts
            likes = driver.find_elements(By.XPATH, "//div[@aria-label='Like' and @role='button']")
            for btn in likes[:2]: # Only the top 2 newest posts to avoid spam filters
                try:
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
                    time.sleep(3)
                    btn.click()
                    print("👍 Found and Liked a new post immediately!")
                except: continue

            # --- ACTION C: THE NAP ---
            # Wait 3-5 minutes before refreshing again. 
            # This 'Immediate' window is the safest speed to avoid account bans.
            nap = random.randint(180, 300)
            print(f"😴 Resting for {nap} seconds...")
            time.sleep(nap)

    except Exception as e:
        print(f"❌ Error in loop: {e}")
        driver.save_screenshot("error_state.png")
    finally:
        driver.quit()

if __name__ == "__main__":
    live_monitor()
