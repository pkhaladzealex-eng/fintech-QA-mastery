## Day 91

---

**Q:** 

Why would you use explicit waits instead of time.sleep()?

**A:** 

Explicit waits check the browser continuously and move forward the moment an element appears, making tests fast and reliable. time.sleep() forces a fixed pause every time, which is slow and fragile. If a page loads in 0.5 seconds, time.sleep(5) wastes 4.5 seconds. If it takes 6 seconds, the test crashes anyway. WebDriverWait adapts to reality. 

---

## Day 92

---

**Q:** Walk me through your testing workflow when you encounter a flaky test that fails randomly.

**A:** First, I check the logs and screenshots from the failure to see if an unexpected element blocked the page. Second, I identify if it's a timing issue—maybe the server was slow that day. I increase explicit wait timeouts or refactor the locators to be more stable. Third, I review the test logic to see if I'm making assumptions about element state. Finally, I run the test multiple times locally to reproduce the issue before declaring it fixed.

---

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

## Day 96

---

**Q:**

"Describe the difference between unit tests and integration tests."

**A:**

"Unit tests verify individual functions in isolation—for example, testing a single helper function. Integration tests verify that multiple components work together correctly—like testing the entire checkout flow from product selection to payment confirmation. Integration tests are closer to real user scenarios but are slower and harder to debug. I use both: unit tests for utility functions, integration tests for complete workflows."

---

 ## Day 97

---

**Q:** 
"Why is negative testing important in QA automation?"

**A:** 
"Positive testing verifies that the happy path works—when everything goes right. Negative testing checks what happens when things go wrong—invalid inputs, failed payments, network errors. Both are critical. If I only test the happy path, I won't catch bugs that affect 10% of users with bad credit cards or slow networks. Negative tests catch edge cases that real users encounter."

---

## Day 101

**Q:** Explain the three layers of automated testing: UI, API, and Database.

**A:** UI testing verifies that the user interface works correctly—buttons click, forms submit, data displays. API testing verifies that backend services process data correctly—payments charge, transactions record. Database testing verifies that data persists correctly—records save, values match. Testing all three together is integration testing. Real bugs often happen at the boundaries between layers, so testing integration is critical.
