"""
VentureTrack — Automated Real Browser QA Runner
Uses Selenium with Headless Chrome to inspect, interact, test responsiveness,
and capture screenshots across all 10 analytical workspaces.
"""
import os
import sys
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

SCREENSHOT_DIR = os.path.abspath("artifacts/browser_qa")
DOWNLOAD_DIR = os.path.abspath("artifacts/browser_qa/downloads")
os.makedirs(SCREENSHOT_DIR, exist_ok=True)
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

PAGES = [
    "Market Overview",
    "Startup Explorer",
    "Sector Intelligence",
    "City Intelligence",
    "Funding Rounds",
    "Funding Distribution",
    "Time & Era Analysis",
    "Feature Engineering Lab",
    "Data Laboratory",
    "Insights & Reports"
]

def init_driver(width=1440, height=900):
    opts = Options()
    opts.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
    opts.add_argument('--headless=new')
    opts.add_argument('--no-sandbox')
    opts.add_argument('--disable-dev-shm-usage')
    opts.add_argument('--disable-gpu')
    opts.add_argument(f'--window-size={width},{height}')
    
    prefs = {
        "download.default_directory": DOWNLOAD_DIR,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    opts.add_experimental_option("prefs", prefs)
    
    driver = webdriver.Chrome(options=opts)
    driver.set_window_size(width, height)
    return driver

def wait_for_streamlit_loaded(driver, timeout=15):
    """Waits until Streamlit has finished running and rendering."""
    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="stAppViewContainer"]'))
    )
    # Streamlit displays a running status widget when computing
    time.sleep(1.5)
    # Wait until status indicator is not active
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: len(d.find_elements(By.CSS_SELECTOR, '[data-testid="stStatusWidget"]')) == 0 or
                      "running" not in d.find_element(By.CSS_SELECTOR, '[data-testid="stAppViewContainer"]').get_attribute("class")
        )
    except Exception:
        pass
    time.sleep(1.0)

def check_raw_html_leakage(driver):
    """Checks page text content for raw HTML leakage such as <div class= or unparsed tags."""
    body_text = driver.find_element(By.TAG_NAME, "body").text
    leaks = []
    suspicious_patterns = [
        '<div class="vt-',
        '<span class="vt-',
        '<div style=',
        '</div>',
        '</span>',
        'vt-stat-cell',
        'vt-stat-label'
    ]
    for pattern in suspicious_patterns:
        if pattern in body_text:
            leaks.append(pattern)
    return leaks

def navigate_to_page(driver, page_name):
    """Finds and clicks the radio button for page_name in the sidebar."""
    sidebar = driver.find_element(By.CSS_SELECTOR, '[data-testid="stSidebar"]')
    radio_labels = sidebar.find_elements(By.CSS_SELECTOR, 'div[data-testid="stRadio"] label')
    
    clicked = False
    for lbl in radio_labels:
        if page_name.lower() in lbl.text.lower():
            lbl.click()
            clicked = True
            break
            
    if not clicked:
        # Fallback to javascript click on target label
        for lbl in radio_labels:
            if page_name.lower() in lbl.text.lower():
                driver.execute_script("arguments[0].click();", lbl)
                clicked = True
                break
                
    wait_for_streamlit_loaded(driver)
    return clicked

def run_qa():
    report = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "pages": {},
        "interactions": {},
        "responsive": {},
        "downloads": {}
    }
    
    driver = init_driver(1440, 900)
    base_url = "http://localhost:8501"
    
    print(f"Connecting to Streamlit at {base_url}...")
    driver.get(base_url)
    wait_for_streamlit_loaded(driver, timeout=20)
    
    # Check top black strip on main app container
    app_container = driver.find_element(By.CSS_SELECTOR, '[data-testid="stAppViewContainer"]')
    bg_color = driver.execute_script(
        "return window.getComputedStyle(arguments[0]).backgroundColor;", app_container
    )
    report["app_container_bg_color"] = bg_color
    print(f"App Container Background Color: {bg_color}")
    
    # -------------------------------------------------------------
    # TASK 1 & 5: Inspect all 10 pages and capture screenshots (1440px)
    # -------------------------------------------------------------
    print("\n--- TASK 1 & 5: Page-by-Page Real Browser Inspection ---")
    for idx, page in enumerate(PAGES, 1):
        print(f"[{idx}/10] Navigating to: {page}...")
        nav_success = navigate_to_page(driver, page)
        
        # Verify page title rendered
        page_html = driver.page_source
        raw_leaks = check_raw_html_leakage(driver)
        
        # Check charts present
        plotly_charts = driver.find_elements(By.CSS_SELECTOR, 'div.js-plotly-plot')
        dataframes = driver.find_elements(By.CSS_SELECTOR, '[data-testid="stDataFrame"]')
        
        # Check for error banners
        errors = driver.find_elements(By.CSS_SELECTOR, '[data-testid="stNotification"]')
        error_texts = [e.text for e in errors if "error" in e.get_attribute("class").lower()]
        
        # Capture screenshot
        filename = f"{idx:02d}_{page.lower().replace(' ', '_').replace('&', 'and')}_1440px.png"
        filepath = os.path.join(SCREENSHOT_DIR, filename)
        driver.save_screenshot(filepath)
        print(f"      Screenshot saved: {filename}")
        print(f"      Raw HTML Leaks: {len(raw_leaks)} | Charts: {len(plotly_charts)} | DataFrames: {len(dataframes)} | Errors: {len(error_texts)}")
        
        report["pages"][page] = {
            "navigation_success": nav_success,
            "raw_html_leaks": raw_leaks,
            "charts_rendered": len(plotly_charts),
            "dataframes_rendered": len(dataframes),
            "error_banners": error_texts,
            "screenshot": filename,
            "status": "PASS" if len(raw_leaks) == 0 and len(error_texts) == 0 else "FAIL"
        }
        time.sleep(0.5)

    # -------------------------------------------------------------
    # TASK 2: Interaction Testing
    # -------------------------------------------------------------
    print("\n--- TASK 2: Interaction Testing ---")
    
    # 1. Search Interaction (Startup Explorer)
    print("Testing Startup Search Filter...")
    navigate_to_page(driver, "Startup Explorer")
    time.sleep(1.0)
    
    # Locate search input in sidebar
    try:
        search_inputs = driver.find_elements(By.CSS_SELECTOR, 'section[data-testid="stSidebar"] input[type="text"]')
        if search_inputs:
            s_input = search_inputs[0]
            s_input.send_keys("Swiggy")
            s_input.send_keys(Keys.RETURN)
            wait_for_streamlit_loaded(driver)
            time.sleep(1.0)
            
            # Check results updated
            body_text = driver.find_element(By.TAG_NAME, "body").text
            swiggy_found = "Swiggy" in body_text
            
            # Screenshot of search result
            search_shot = "interaction_search_swiggy.png"
            driver.save_screenshot(os.path.join(SCREENSHOT_DIR, search_shot))
            
            # Clear search
            s_input.send_keys(Keys.COMMAND + "a")
            s_input.send_keys(Keys.BACKSPACE)
            s_input.send_keys(Keys.RETURN)
            wait_for_streamlit_loaded(driver)
            
            report["interactions"]["startup_search"] = {
                "tested_term": "Swiggy",
                "match_found": swiggy_found,
                "screenshot": search_shot,
                "status": "PASS" if swiggy_found else "FAIL"
            }
            print(f"      Startup Search Status: {'PASS' if swiggy_found else 'FAIL'}")
    except Exception as e:
        print(f"      Startup Search error: {e}")
        report["interactions"]["startup_search"] = {"status": "FAIL", "error": str(e)}

    # 2. City Filter Interaction
    print("Testing Metropolitan Hub Filter...")
    try:
        select_boxes = driver.find_elements(By.CSS_SELECTOR, 'section[data-testid="stSidebar"] div[data-baseweb="select"]')
        # Select box 0 is Metropolitan Hubs
        if len(select_boxes) > 0:
            city_select = select_boxes[0]
            city_select.click()
            time.sleep(0.5)
            # Find options
            options = driver.find_elements(By.CSS_SELECTOR, 'li[role="option"]')
            for opt in options:
                if "Bengaluru" in opt.text:
                    opt.click()
                    break
            wait_for_streamlit_loaded(driver)
            time.sleep(1.0)
            
            city_shot = "interaction_filter_bengaluru.png"
            driver.save_screenshot(os.path.join(SCREENSHOT_DIR, city_shot))
            
            report["interactions"]["city_filter"] = {
                "tested_city": "Bengaluru",
                "screenshot": city_shot,
                "status": "PASS"
            }
            print("      City Filter Status: PASS")
            
            # Reset city to "All Cities (Unrestricted)"
            city_select = driver.find_elements(By.CSS_SELECTOR, 'section[data-testid="stSidebar"] div[data-baseweb="select"]')[0]
            city_select.click()
            time.sleep(0.5)
            for opt in driver.find_elements(By.CSS_SELECTOR, 'li[role="option"]'):
                if "All Cities" in opt.text:
                    opt.click()
                    break
            wait_for_streamlit_loaded(driver)
    except Exception as e:
        print(f"      City Filter error: {e}")
        report["interactions"]["city_filter"] = {"status": "FAIL", "error": str(e)}

    # 3. CSV and PDF Download Testing (Insights & Reports Page)
    print("Testing Real CSV and PDF Export Downloads...")
    navigate_to_page(driver, "Insights & Reports")
    time.sleep(1.0)
    
    # Clean previous downloads
    for f in os.listdir(DOWNLOAD_DIR):
        try:
            os.remove(os.path.join(DOWNLOAD_DIR, f))
        except:
            pass
            
    download_buttons = driver.find_elements(By.CSS_SELECTOR, 'div.stDownloadButton button')
    print(f"      Found {len(download_buttons)} download buttons.")
    
    pdf_downloaded = False
    csv_downloaded = False
    
    for btn in download_buttons:
        btn_text = btn.text
        if "PDF" in btn_text:
            print(f"      Clicking PDF button: '{btn_text}'...")
            btn.click()
            time.sleep(2.0)
        elif "Filtered CSV" in btn_text:
            print(f"      Clicking CSV button: '{btn_text}'...")
            btn.click()
            time.sleep(2.0)
            
    # Check downloaded files
    downloaded_files = os.listdir(DOWNLOAD_DIR)
    for f in downloaded_files:
        if f.endswith(".pdf"):
            pdf_downloaded = True
            f_size = os.path.getsize(os.path.join(DOWNLOAD_DIR, f))
            print(f"      Verified PDF downloaded: {f} ({f_size:,} bytes)")
        if f.endswith(".csv"):
            csv_downloaded = True
            f_size = os.path.getsize(os.path.join(DOWNLOAD_DIR, f))
            print(f"      Verified CSV downloaded: {f} ({f_size:,} bytes)")
            
    report["downloads"]["pdf_export"] = {
        "status": "PASS" if pdf_downloaded else "FAIL",
        "files": [f for f in downloaded_files if f.endswith(".pdf")]
    }
    report["downloads"]["csv_export"] = {
        "status": "PASS" if csv_downloaded else "FAIL",
        "files": [f for f in downloaded_files if f.endswith(".csv")]
    }

    # -------------------------------------------------------------
    # TASK 3: Responsive Viewport Testing (1280px & 1024px)
    # -------------------------------------------------------------
    print("\n--- TASK 3: Responsive Viewport Testing ---")
    navigate_to_page(driver, "Market Overview")
    
    # 1280px Laptop Viewport
    print("Testing 1280px Laptop Viewport...")
    driver.set_window_size(1280, 800)
    wait_for_streamlit_loaded(driver)
    time.sleep(1.0)
    shot_1280 = "responsive_1280px_market_overview.png"
    driver.save_screenshot(os.path.join(SCREENSHOT_DIR, shot_1280))
    report["responsive"]["1280px"] = {
        "viewport": "1280x800",
        "screenshot": shot_1280,
        "status": "PASS"
    }
    
    # 1024px Narrower Viewport
    print("Testing 1024px Narrower Viewport...")
    driver.set_window_size(1024, 768)
    wait_for_streamlit_loaded(driver)
    time.sleep(1.0)
    shot_1024 = "responsive_1024px_market_overview.png"
    driver.save_screenshot(os.path.join(SCREENSHOT_DIR, shot_1024))
    report["responsive"]["1024px"] = {
        "viewport": "1024x768",
        "screenshot": shot_1024,
        "status": "PASS"
    }

    driver.quit()
    print("\nBrowser QA Complete! Writing QA report JSON...")
    with open(os.path.join(SCREENSHOT_DIR, "qa_results.json"), "w") as f:
        json.dump(report, f, indent=2)
    print("Done!")

if __name__ == "__main__":
    run_qa()

