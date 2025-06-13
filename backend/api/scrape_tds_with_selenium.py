import time
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# Setup headless Chrome
options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

BASE_URL = "https://tds.s-anand.net/#/README"  # ✅ Use README to ensure sidebar loads
OUTPUT_DIR = "backend/data/tds_course_dynamic"
os.makedirs(OUTPUT_DIR, exist_ok=True)

print(f"🌐 Opening {BASE_URL}")
driver.get(BASE_URL)

# Wait for sidebar to load
WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, ".sidebar-nav a"))
)

# ✅ Dump full HTML for debug
with open("debug_full_page.html", "w", encoding="utf-8") as f:
    f.write(driver.page_source)
print("📄 Dumped full HTML to debug_full_page.html")

# Extract sidebar links
sidebar_links = driver.find_elements(By.CSS_SELECTOR, ".sidebar-nav a")
print(f"🔗 Found {len(sidebar_links)} links in sidebar")

for idx in range(len(sidebar_links)):
    # Re-fetch sidebar links on each iteration to avoid stale element errors
    sidebar_links = driver.find_elements(By.CSS_SELECTOR, ".sidebar-nav a")
    link = sidebar_links[idx]

    section_name = link.get_attribute("title") or link.text.strip()
    href = link.get_attribute("href")

    if not section_name or not href or not href.startswith("https://tds.s-anand.net/#/"):
        continue

    print(f"[{idx+1}] Navigating to: {section_name} ({href})")
    driver.get(href)
    time.sleep(2)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    content_div = soup.find("main") or soup.find("div", class_="content")

    if content_div:
        content = content_div.get_text(separator="\n", strip=True)
    else:
        content = soup.get_text(separator="\n", strip=True)

    safe_name = section_name.replace(" ", "_").replace("/", "_").replace(":", "")
    filepath = os.path.join(OUTPUT_DIR, f"{safe_name}.txt")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✅ Saved {safe_name}.txt")


driver.quit()
print("🎉 Done scraping all sidebar content.")

