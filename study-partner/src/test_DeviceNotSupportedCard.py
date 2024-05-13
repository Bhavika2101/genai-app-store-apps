# ********RoostGPT********
"""
Test generated by RoostGPT for test python-unit-studypartner using AI Type Open AI and AI Model gpt-4

ROOST_METHOD_HASH=device_not_supported_card_9fa9f4ae8a
ROOST_METHOD_SIG_HASH=device_not_supported_card_f06272b12e

```
Scenario 1: Test if the function returns a form card
Details:
  TestName: test_returns_form_card
  Description: This test is intended to verify if the function returns a form card. The form card is the expected return type of the function.
Execution:
  Arrange: No arrangement is necessary as the function does not require any parameters.
  Act: Invoke the function without passing any parameters.
  Assert: Check if the returned result is a form card.
Validation:
  The function's purpose is to return a form card. Thus this test is important to verify if the function is performing its intended operation.

Scenario 2: Test the form card box ID
Details:
  TestName: test_form_card_box_id
  Description: This test is intended to verify if the form card returned by the function has the correct box ID. The box ID is expected to be "device-not-supported".
Execution:
  Arrange: No arrangement is necessary as the function does not require any parameters.
  Act: Invoke the function without passing any parameters.
  Assert: Check if the box ID of the returned form card is "device-not-supported".
Validation:
  The box ID is essential for the form card to be displayed correctly on the user interface. Hence, it is important to verify if the function is setting the correct box ID.

Scenario 3: Test the form card content
Details:
  TestName: test_form_card_content
  Description: This test is intended to verify if the form card returned by the function contains the correct content. The content is expected to be a text saying "This app was built desktop; it is not available on mobile or tablets."
Execution:
  Arrange: No arrangement is necessary as the function does not require any parameters.
  Act: Invoke the function without passing any parameters.
  Assert: Check if the content of the returned form card is the expected text.
Validation:
  The content of the form card is what the user sees on the user interface. Therefore, it is important to verify if the function is setting the correct content.
```
"""

# ********RoostGPT********
import os
from h2o_wave import ui, Q, data
from cards import device_not_supported_card
import pytest

class Test_DeviceNotSupportedCard:
    def test_returns_form_card(self):
        result = device_not_supported_card()
        assert isinstance(result, ui.form_card)
        
    def test_form_card_box_id(self):
        result = device_not_supported_card()
        assert result.box == "device-not-supported"

    def test_form_card_content(self):
        result = device_not_supported_card()
        assert result.items[0].content == "This app was built desktop; it is not available on mobile or tablets."
 