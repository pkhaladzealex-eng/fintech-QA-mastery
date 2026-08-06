## Day 91

---

**Q:** Why would you use explicit waits instead of time.sleep()?

**A:** Explicit waits check the browser continuously and move forward the moment an element appears, making tests fast and reliable. time.sleep() forces a fixed pause every time, which is slow and fragile. If a page loads in 0.5 seconds, time.sleep(5) wastes 4.5 seconds. If it takes 6 seconds, the test crashes anyway. WebDriverWait adapts to reality. 

## Day 92

---

**Q:** Walk me through your testing workflow when you encounter a flaky test that fails randomly.

**A:** First, I check the logs and screenshots from the failure to see if an unexpected element blocked the page. Second, I identify if it's a timing issue—maybe the server was slow that day. I increase explicit wait timeouts or refactor the locators to be more stable. Third, I review the test logic to see if I'm making assumptions about element state. Finally, I run the test multiple times locally to reproduce the issue before declaring it fixed.

---