import requests
import warnings
import time
import os
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from colorama import Fore
from pystyle import Center, Colors, Colorate

warnings.filterwarnings("ignore", category=DeprecationWarning)

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def banner():
    clear()
    os.system("title Twitch Viewer Bot - Enhanced Version by PrimeEcto")
    print(Colorate.Vertical(Colors.green_to_cyan, Center.XCenter(""" 
 /$$$$$$$  /$$$$$$$  /$$$$$$ /$$      /$$ /$$$$$$$$ /$$$$$$$$  /$$$$$$  /$$$$$$$$ /$$$$$$ 
| $$__  $$| $$__  $$|_  $$_/| $$$    /$$$| $$_____/| $$_____/ /$$__  $$|__  $$__//$$__  $$ 
| $$  \ $$| $$  \ $$  | $$  | $$$$  /$$$$| $$      | $$      | $$  \__/   | $$  | $$  \ $$ 
| $$$$$$$/| $$$$$$$/  | $$  | $$ $$/$$ $$| $$$$$   | $$$$$   | $$         | $$  | $$  | $$ 
| $$____/ | $$__  $$  | $$  | $$  $$$| $$| $$__/   | $$__/   | $$         | $$  | $$  | $$ 
| $$      | $$  \ $$  | $$  | $$\  $ | $$| $$      | $$      | $$    $$   | $$  | $$  | $$ 
| $$      | $$  | $$ /$$$$$$| $$ \/  | $$| $$$$$$$$| $$$$$$$$|  $$$$$$/   | $$  |  $$$$$$/ 
|__/      |__/  |__/|______/|__/     |__/|________/|________/ \______/    |__/   \______/ 

PrimeEcto Viewer Bot — Enhanced Stability Version!
""")))

def check_for_updates():
    return True

def print_announcement():
    return "Welcome to the Enhanced Twitch Viewer Bot by PrimeEcto! Improved stability and viewer retention."

def simulate_viewer_activity(driver, viewer_index):
    try:
        # More natural scrolling behavior
        scroll_amount = random.randint(100, 500)
        driver.execute_script(f"window.scrollTo(0, {scroll_amount});")
        time.sleep(random.uniform(2, 4))
        
        # Simulate mouse movement
        driver.execute_script("""
            var event = new MouseEvent('mousemove', {
                'view': window,
                'bubbles': true,
                'cancelable': true,
                'clientX': arguments[0],
                'clientY': arguments[1]
            });
            document.dispatchEvent(event);
        """, random.randint(100, 800), random.randint(100, 600))
        
        # Quality changes to appear more human-like
        if random.random() < 0.3:  # 30% chance
            quality_options = ['160p', '360p', '480p', '720p']
            selected_quality = random.choice(quality_options)
            driver.execute_script(f"document.querySelector('.quality-picker-button')?.click();")
            time.sleep(1)
            driver.execute_script(f"document.querySelector('[data-quality=\"{selected_quality}\"]')?.click();")
        
        # Random interaction with player
        if random.random() < 0.2:  # 20% chance
            driver.execute_script("""
                var video = document.querySelector('video');
                if(video) {
                    if(video.paused) {
                        video.play();
                    } else {
                        video.currentTime += Math.random() * 10;
                    }
                }
            """)
            
        time.sleep(random.uniform(8, 20))
    except Exception as e:
        print(f"Activity simulation error for viewer {viewer_index}: {e}")

def setup_chrome_options(headless=False):
    chrome_options = webdriver.ChromeOptions()
    
    # Enhanced stealth settings
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # Performance optimizations
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-software-rasterizer')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-infobars')
    chrome_options.add_argument('--disable-notifications')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--mute-audio')
    
    # Memory optimization
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--disable-popup-blocking')
    chrome_options.add_argument('--disable-default-apps')
    
    # Random viewport size for each instance
    width = random.randint(1024, 1920)
    height = random.randint(768, 1080)
    chrome_options.add_argument(f'--window-size={width},{height}')
    
    # Randomized user agent
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"
    ]
    chrome_options.add_argument(f'user-agent={random.choice(user_agents)}')
    
    if headless:
        chrome_options.add_argument('--headless')
    
    return chrome_options

def main():
    if not check_for_updates():
        return

    announcement = print_announcement()
    banner()
    print(Colors.red, Center.XCenter("ANNOUNCEMENT"))
    print(Colors.yellow, Center.XCenter(f"{announcement}"))
    print()

    proxy_servers = {
        1: "https://www.croxyproxy.com",
        2: "https://www.croxyproxy.rocks",
        3: "https://www.croxy.network",
        4: "https://www.croxy.org",
        5: "https://www.croxyproxy.net",
        6: "https://www.blockaway.net",
        7: "https://www.youtubeunblocked.live",
    }

    print(Colors.green, Center.XCenter("Proxy Server 1 (CroxyProxy.com) is Recommended"))
    print()
    for i in range(1, 8):
        print(Colorate.Vertical(Colors.green_to_blue, f"Proxy Server {i}: {proxy_servers[i]}"))

    proxy_choice = int(input("\nEnter Proxy Server Number: "))
    proxy_url = proxy_servers.get(proxy_choice, proxy_servers[1])

    twitch_username = input("Enter your Twitch channel name (e.g. PrimeEcto): ")
    viewer_count = int(input("How many viewers to simulate? (open windows): "))
    
    if viewer_count > 15:
        print("\nWarning: Running more than 15 viewers might cause instability.")
        confirm = input("Continue anyway? (y/n): ").lower()
        if confirm != 'y':
            return

    headless_mode = input("Run in headless mode (no windows visible)? (y/n): ").strip().lower()
    headless = headless_mode == "y"

    print("\nChoose launch mode:")
    print("1. Stealth Mode (realistic & more stable)")
    print("2. Rapid Mode (faster but may be less stable)")
    mode_choice = input("Enter mode number (1 or 2): ").strip()
    rapid_mode = mode_choice == "2"

    clear()
    banner()
    print(Colors.green, Center.XCenter("Initializing viewers... Please wait."))

    drivers = []
    try:
        for i in range(viewer_count):
            chrome_options = setup_chrome_options(headless)
            
            try:
                driver = webdriver.Chrome(options=chrome_options)
                drivers.append(driver)
                
                driver.get(proxy_url)
                
                # Wait for URL input field with timeout
                wait = WebDriverWait(driver, 20)
                text_box = wait.until(EC.presence_of_element_located((By.ID, 'url')))
                
                # Add randomized delay between keystrokes
                twitch_url = f'https://www.twitch.tv/{twitch_username}'
                for char in twitch_url:
                    text_box.send_keys(char)
                    time.sleep(random.uniform(0.1, 0.3))
                
                text_box.send_keys(Keys.RETURN)
                
                print(f"Viewer {i + 1}/{viewer_count} initialized successfully")
                
                if not rapid_mode:
                    time.sleep(random.uniform(3, 7))
                    simulate_viewer_activity(driver, i)
                
            except Exception as e:
                print(f"Error initializing viewer {i + 1}: {e}")
                continue
            
        print("\nAll viewers initialized. Press Ctrl+C to stop and close all viewers.")
        
        # Continuous activity simulation
        while True:
            for i, driver in enumerate(drivers):
                try:
                    simulate_viewer_activity(driver, i)
                    time.sleep(random.uniform(1, 3))
                except:
                    continue
            
    except KeyboardInterrupt:
        print("\nShutting down viewers...")
    finally:
        for driver in drivers:
            try:
                driver.quit()
            except:
                continue

if __name__ == "__main__":
    main()