import os
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def setup_driver():
    options = Options()
    # Essential for GitHub Actions
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    # Masking the bot as a real Chrome user
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36")
    return webdriver.Chrome(options=options)

def run_bot():
    driver = setup_driver()
    wait = WebDriverWait(driver, 20)
    
    try:
        print("🚀 Navigating to Facebook...")
        driver.get("https://www.facebook.com")
        
        # 1. Handle potential Cookie Consent
        try:
            cookie_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Allow') or contains(., 'Accept')]")))
            cookie_btn.click()
            print("✅ Cookies accepted.")
        except:
            print("ℹ️ No cookie pop-up found.")

        # 2. Login Process
        print("🔑 Attempting login...")
        email_field = wait.until(EC.presence_of_element_located((By.ID, "email")))
        email_field.send_keys("0746404008")
        
        pass_field = driver.find_element(By.ID, "pass")
        pass_field.send_keys("val8525")
        pass_field.send_keys(Keys.RETURN)
        
        # Wait to let the homepage load
        time.sleep(10)

        # 3. Like Posts in Feed
        print("📱 Interacting with feed...")
        for i in range(3):
            # Scroll down to load content
            driver.execute_script(f"window.scrollBy(0, {random.randint(700, 1000)});")
            time.sleep(random.uniform(3, 6))
            
            try:
                # Target the 'Like' button via aria-label
                likes = driver.find_elements(By.XPATH, "//div[@aria-label='Like' and @role='button']")
                if likes:
                    likes[0].click()
                    print(f"👍 Liked post {i+1}.")
            except Exception as e:
                print(f"⚠️ Could not like post: {e}")

        # 4. View Stories
        print("📖 Viewing stories...")
        try:
            story_tray = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Stories']//div[@role='link']")))
            story_tray.click()
            
            for s in range(5):
                print(f"👀 Watching story {s+1}...")
                # Watch for a realistic duration
                time.sleep(random.uniform(7, 12))
                
                # Click 'Next' to move to the next story
                next_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Next card']")))
                next_btn.click()
        except Exception as e:
            print(f"⚠️ Story interaction ended: {e}")

        print("✨ All tasks finished successfully!")

    except Exception as e:
        print(f"❌ CRITICAL ERROR: {e}")
        driver.save_screenshot("fail_screenshot.png")
        print("📸 Failure screenshot saved.")
        raise e 
    finally:
        driver.quit()

if __name__ == "__main__":
    run_bot()
