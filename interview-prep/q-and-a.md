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

---

**Q:** Explain the three layers of automated testing: UI, API, and Database.

**A:** UI testing verifies that the user interface works correctly—buttons click, forms submit, data displays. API testing verifies that backend services process data correctly—payments charge, transactions record. Database testing verifies that data persists correctly—records save, values match. Testing all three together is integration testing. Real bugs often happen at the boundaries between layers, so testing integration is critical.

---

## Day 102

---


**Q:**

"How do you test error scenarios in integration tests?"

**:**

"I test both happy path and error paths. For error scenarios, I use test data that triggers failures—like declined payment cards, invalid inputs, network timeouts. I verify that errors are handled gracefully: the UI shows error messages, the API returns correct error codes, and the database records the failed state. Testing error paths catches bugs that real users experience 10% of the time."

---

## Day 104

---

**Q:**

"How would you approach testing a completely new e-commerce platform you've never seen?"

**A:**

"First, I'd explore the site manually to understand the checkout flow—what fields exist, what validations occur. Then I'd identify stable locators (IDs are better than classes because they change less). I'd start with one happy-path test to verify the framework works. Then I'd add edge cases—invalid inputs, missing fields, different payment methods. Finally, I'd organize code by platform in separate folders so each site's tests are isolated."

---

## Day 105

---

**Q:**

"What's the difference between testing an API directly vs testing it through the UI?"

**A:**

"Testing API directly is faster and more focused. I test specific endpoints without waiting for UI rendering. I can test edge cases that the UI doesn't expose. But I miss integration bugs that only happen through the UI. So I do both: API tests for backend logic, UI tests for user experience. Together they catch all bugs."

---

## Day 106

---

**Interview Question:**

"Explain what CI/CD means and why it matters for QA."

**Answer to memorize:**

"CI/CD stands for Continuous Integration and Continuous Deployment. CI means code changes are automatically tested as soon as pushed. CD means validated code is automatically deployed. For QA, CI/CD is critical because it catches bugs early—before they reach production. Automated tests run on every commit, ensuring code quality stays high. This is industry standard in all modern tech companies."

---

