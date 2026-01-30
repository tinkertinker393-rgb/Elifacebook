import time
import random
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
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36")
    return webdriver.Chrome(options=options)

def run_bot():
    driver = setup_driver()
    wait = WebDriverWait(driver, 20)
    
    try:
        print("🚀 Navigating to Facebook...")
        driver.get("https://www.facebook.com")
        
        # 1. Login
        print("🔑 Logging in...")
        email_field = wait.until(EC.presence_of_element_located((By.ID, "email")))
        email_field.send_keys("0746404008")
        pass_field = driver.find_element(By.ID, "pass")
        pass_field.send_keys("val8525")
        pass_field.send_keys(Keys.RETURN)
        time.sleep(10)

        # 2. React to Feed Posts
        print("📱 Interacting with feed...")
        for i in range(50):
            driver.execute_script(f"window.scrollBy(0, {random.randint(800, 1100)});")
            time.sleep(random.uniform(4, 7))
            try:
                # This finds the Like button
                like_btn = driver.find_elements(By.XPATH, "//div[@aria-label='Like' and @role='button']")
                if like_btn:
                    # To "Love" instead of "Like", you click and hold, but for simplicity, we click Like.
                    driver.execute_script("arguments[0].click();", like_btn[0])
                    print(f"👍 Liked post {i+1}")
            except:
                continue

        # 3. View and React to Stories
        print("📖 Opening stories...")
        try:
            story_tray = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Stories']//div[@role='link']")))
            story_tray.click()
            
            for s in range(50): # Watch up to 10 stories
                time.sleep(random.uniform(7, 12))
                
                # Attempt to 'Like' (Heart) the story
                try:
                    # Targets the heart icon/react button inside story viewer
                    react_btn = driver.find_element(By.XPATH, "//div[@aria-label='Like' or @aria-label='React' or @aria-label='Give a Heart']//div[@role='button']")
                    react_btn.click()
                    print(f"❤️ Loved story {s+1}")
                except:
                    pass

                # Move to next story using keyboard (most reliable)
                ActionChains(driver).send_keys(Keys.ARROW_RIGHT).perform()
        except:
            print("ℹ️ Finished viewing stories.")

    except Exception as e:
        print(f"❌ Error: {e}")
        driver.save_screenshot("fail_screenshot.png")
    finally:
        print("🔒 Closing session.")
        driver.quit()

if __name__ == "__main__":
    run_bot()
