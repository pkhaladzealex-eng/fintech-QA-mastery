## Day 91

---

**Q:** 

Why would you use explicit waits instead of time.sleep()?

**A:** 

Explicit waits check the browser continuously and move forward the moment an element appears, making tests fast and reliable. time.sleep() forces a fixed pause every time, which is slow and fragile. If a page loads in 0.5 seconds, time.sleep(5) wastes 4.5 seconds. If it takes 6 seconds, the test crashes anyway. WebDriverWait adapts to reality. 

## Day 92

---

**Q:** Walk me through your testing workflow when you encounter a flaky test that fails randomly.

**A:** First, I check the logs and screenshots from the failure to see if an unexpected element blocked the page. Second, I identify if it's a timing issue—maybe the server was slow that day. I increase explicit wait timeouts or refactor the locators to be more stable. Third, I review the test logic to see if I'm making assumptions about element state. Finally, I run the test multiple times locally to reproduce the issue before declaring it fixed.

## Day 94

---

**Q:** 

"How do you organize test code to avoid duplication?"

**A:** 

"I create helper functions in separate utility files for repeated actions—like login, add_to_cart, navigate_to_checkout. Then in my test files, I import and reuse these helpers. This follows DRY principle (Don't Repeat Yourself) and makes tests easier to maintain. If a UI element changes, I update the helper once, not in 10 different tests."

---

## Day 95

---

**Q:**

"How do you handle dynamic content or delays in web automation?"

**A:**

"I use explicit waits with expected conditions instead of hardcoded sleeps. WebDriverWait checks the DOM continuously until the condition is met or timeout occurs. For dynamic XPath expressions, I use f-strings to parameterize values. For JavaScript-heavy sites, I sometimes wait for elements to be stale before checking new content to ensure the page has fully refreshed."

---

