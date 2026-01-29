#!/usr/bin/env python3
"""
Scraper Template
Copy and modify this for new public image databases

Part of HeadCount: https://github.com/[username]/headcount
"""

import os
import sys
import time

try:
    import requests
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
except ImportError:
    print("Missing dependencies. Install with:")
    print("  pip install selenium webdriver-manager requests --break-system-packages")
    sys.exit(1)


# ============================================================
# CONFIGURATION - Edit these for your target
# ============================================================

TARGET_URL = "https://example.gov/public-database"
OUTPUT_DIR = "scraped_photos"

# CSS selectors or XPaths for finding images
IMAGE_SELECTOR = "img.mugshot"  # or use By.XPATH

# Pagination button (if any)
NEXT_BUTTON_TEXT = "Next"  # or "Show More", "Load More", etc.

# Optional: filter images by URL pattern
IMAGE_URL_FILTER = None  # e.g., "mugshot" or "photo"


# ============================================================
# SCRAPER - Modify as needed
# ============================================================

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Setup browser
    options = Options()
    # options.add_argument('--headless')  # Uncomment to run hidden
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    
    print(f"Starting browser...")
    print(f"Target: {TARGET_URL}")
    
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), 
        options=options
    )
    
    driver.get(TARGET_URL)
    time.sleep(5)  # Wait for page to load
    
    photo_count = 0
    page = 1
    saved_urls = set()
    
    while True:
        print(f'\nPage {page}...')
        
        # Find images - modify selector as needed
        try:
            images = driver.find_elements(By.CSS_SELECTOR, IMAGE_SELECTOR)
        except:
            images = driver.find_elements(By.TAG_NAME, 'img')
        
        print(f'  Found {len(images)} images')
        
        for img in images:
            src = img.get_attribute('src')
            if not src or src in saved_urls:
                continue
            
            # Optional URL filter
            if IMAGE_URL_FILTER and IMAGE_URL_FILTER not in src.lower():
                continue
            
            try:
                saved_urls.add(src)
                
                # Download image
                resp = requests.get(src, timeout=15, verify=False)
                
                if resp.status_code == 200 and len(resp.content) > 1000:
                    photo_count += 1
                    
                    # Detect extension
                    ext = 'jpg'
                    if '.png' in src.lower():
                        ext = 'png'
                    
                    filename = f'{OUTPUT_DIR}/photo_{photo_count:04d}.{ext}'
                    with open(filename, 'wb') as f:
                        f.write(resp.content)
                    print(f'  Saved: {filename}')
                    
            except Exception as e:
                print(f'  Error downloading: {e}')
        
        # Try to click next/more button
        clicked = False
        if NEXT_BUTTON_TEXT:
            try:
                buttons = driver.find_elements(
                    By.XPATH, 
                    f"//*[contains(text(), '{NEXT_BUTTON_TEXT}')]"
                )
                for btn in buttons:
                    if btn.is_displayed() and btn.is_enabled():
                        driver.execute_script("arguments[0].click();", btn)
                        print(f'  Clicked "{NEXT_BUTTON_TEXT}"')
                        clicked = True
                        time.sleep(3)
                        break
            except Exception as e:
                print(f'  Pagination error: {e}')
        
        # Also try scrolling (for infinite scroll pages)
        if not clicked:
            old_height = driver.execute_script('return document.body.scrollHeight')
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            time.sleep(2)
            new_height = driver.execute_script('return document.body.scrollHeight')
            if new_height > old_height:
                clicked = True
                print('  Scrolled to load more')
        
        page += 1
        
        # Stop conditions
        if page > 100:
            print('Reached page limit')
            break
        
        if not clicked:
            print('No more content to load')
            break
    
    print(f'\n{"="*50}')
    print(f'COMPLETE!')
    print(f'Total photos: {photo_count}')
    print(f'Output: {OUTPUT_DIR}/')
    print(f'{"="*50}')
    print(f'\nNext: python3 headcount.py --input {OUTPUT_DIR}')
    
    driver.quit()


if __name__ == "__main__":
    main()
