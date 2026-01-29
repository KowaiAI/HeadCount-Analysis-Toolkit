#!/usr/bin/env python3
"""
DC Sex Offender Registry Scraper
Scrapes mugshots from sexoffender.dc.gov

Part of HeadCount: https://github.com/[username]/headcount
"""

import os
import sys
import time
import urllib3

# Disable SSL warnings (CSOSA has cert issues)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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

OUTPUT_DIR = "dc_photos"


def main():
    """Scrape and download images from the DC Sex Offender Registry.
    
    This function initializes a web driver to navigate to the DC Sex Offender
    Registry,  scrapes images from the site, and downloads them to a specified
    output directory.  It handles pagination by clicking the "Show More" button
    until a set page limit is reached  or no more images are available. The
    function also manages SSL verification during downloads  and tracks saved image
    URLs to avoid duplicates.
    """
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║  DC Sex Offender Registry Scraper                         ║
    ║  Part of HeadCount                                        ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Setup browser
    options = Options()
    # options.add_argument('--headless')  # Uncomment to run hidden
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    
    print("Starting browser...")
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), 
        options=options
    )
    
    driver.get('https://sexoffender.dc.gov/search/all')
    time.sleep(5)
    
    photo_count = 0
    page = 1
    saved_urls = set()
    
    while True:
        print(f'\nPage {page}...')
        
        # Find all images
        images = driver.find_elements(By.TAG_NAME, 'img')
        print(f'  Found {len(images)} images')
        
        for img in images:
            src = img.get_attribute('src')
            if not src or src in saved_urls:
                continue
            
            # Only get CSOSA mugshots
            if 'sor.csosa.net' in src or 'ViewImage' in src:
                try:
                    saved_urls.add(src)
                    
                    # Download with SSL verification disabled
                    resp = requests.get(src, timeout=15, verify=False)
                    
                    if resp.status_code == 200 and len(resp.content) > 1000:
                        photo_count += 1
                        filename = f'{OUTPUT_DIR}/photo_{photo_count:04d}.jpg'
                        with open(filename, 'wb') as f:
                            f.write(resp.content)
                        print(f'  Saved: {filename} ({len(resp.content)} bytes)')
                        
                except Exception as e:
                    print(f'  Error: {e}')
        
        # Click "Show More" button
        clicked = False
        try:
            buttons = driver.find_elements(By.XPATH, "//*[contains(text(), 'Show More')]")
            for btn in buttons:
                if btn.is_displayed() and btn.is_enabled():
                    driver.execute_script("arguments[0].click();", btn)
                    print(f'  Clicked "Show More"')
                    clicked = True
                    time.sleep(3)
                    break
        except Exception as e:
            print(f'  Button error: {e}')
        
        page += 1
        
        # Stop conditions
        if page > 200:
            print('Reached page limit')
            break
        
        if not clicked:
            print('No more "Show More" button found - done!')
            break
    
    print(f'\n{"="*60}')
    print(f'COMPLETE!')
    print(f'Total photos saved: {photo_count}')
    print(f'Saved to: {OUTPUT_DIR}/')
    print(f'{"="*60}')
    print(f'\nNext step: python3 headcount.py')
    
    input('\nPress Enter to close browser...')
    driver.quit()


if __name__ == "__main__":
    main()
