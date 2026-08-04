## Day 91

**Q:** Why would you use explicit waits instead of time.sleep()?

**A:** Explicit waits check the browser continuously and move forward the moment an element appears, making tests fast and reliable. time.sleep() forces a fixed pause every time, which is slow and fragile. If a page loads in 0.5 seconds, time.sleep(5) wastes 4.5 seconds. If it takes 6 seconds, the test crashes anyway. WebDriverWait adapts to reality. 
