# ********RoostGPT********
"""
Test generated by RoostGPT for test python-unit-studypartner using AI Type Open AI and AI Model gpt-4

ROOST_METHOD_HASH=device_not_supported_card_9fa9f4ae8a
ROOST_METHOD_SIG_HASH=device_not_supported_card_f06272b12e

================================================================================
Scenario 1: Verify the type of card returned by the function
Details:
  TestName: test_returned_card_type
  Description: This test is intended to verify that the function device_not_supported_card is returning a form card. The business logic encapsulated by the function is to return a form card to the caller.
Execution:
  Arrange: No setup is required as the function does not take any parameters.
  Act: Invoke the function without any parameters.
  Assert: Check that the returned object is an instance of ui.form_card.
Validation:
  The test confirms the function's specification to return a form card. It is important to ensure that the function is returning the correct type of card, which is a form card in this case.

Scenario 2: Verify the box of the returned card
Details:
  TestName: test_returned_card_box
  Description: This test is intended to verify that the box of the returned form card is "device-not-supported". The business logic encapsulated by the function is to return a form card with a specific box.
Execution:
  Arrange: No setup is required as the function does not take any parameters.
  Act: Invoke the function without any parameters.
  Assert: Check that the box of the returned form card is "device-not-supported".
Validation:
  This test checks the function's specification to return a form card with a specific box. It is important to ensure that the function is returning a form card with the correct box.

Scenario 3: Verify the items of the returned card
Details:
  TestName: test_returned_card_items
  Description: This test is intended to verify that the items of the returned form card contain a single text item with a specific message. The business logic encapsulated by the function is to return a form card with a specific item.
Execution:
  Arrange: No setup is required as the function does not take any parameters.
  Act: Invoke the function without any parameters.
  Assert: Check that the items of the returned form card contain a single text item with the message "This app was built desktop; it is not available on mobile or tablets."
Validation:
  This test checks the function's specification to return a form card with a specific item. It is important to ensure that the function is returning a form card with the correct items.
"""

# ********RoostGPT********
import os
from h2o_wave import ui, Q, data
from cards import device_not_supported_card
import pytest

class Test_CardsDeviceNotSupportedCard:

    def test_returned_card_type(self):
        card = device_not_supported_card()
        assert isinstance(card, ui.form_card), "Returned card is not of type form_card"

    def test_returned_card_box(self):
        card = device_not_supported_card()
        assert card.box == "device-not-supported", "The box of the returned card is not 'device-not-supported'"

    def test_returned_card_items(self):
        card = device_not_supported_card()
        assert len(card.items) == 1, "The returned card does not contain exactly one item"
        assert isinstance(card.items[0], ui.text_xl), "The item of the returned card is not of type text_xl"
        assert card.items[0].content == "This app was built desktop; it is not available on mobile or tablets.", "The item of the returned card does not contain the expected message"
