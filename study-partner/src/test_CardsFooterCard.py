# ********RoostGPT********
"""
Test generated by RoostGPT for test python-unit-studypartner using AI Type Open AI and AI Model gpt-4

ROOST_METHOD_HASH=footer_card_062d99a4b9
ROOST_METHOD_SIG_HASH=footer_card_3e136a9ae6

```
Scenario 1: Validate the footer_card function's return type
Details:
  TestName: test_footer_card_return_type
  Description: This test is intended to verify that the return type of the footer_card function is ui.Card.
Execution:
  Arrange: No setup is required as the function does not take any arguments.
  Act: Invoke the footer_card function.
  Assert: Check whether the returned object is an instance of ui.Card.
Validation:
  This test is important as the function is expected to return a ui.Card object. Ensuring this will help confirm that the function behaves as expected and returns the correct type of object.

Scenario 2: Validate the box attribute of the returned ui.Card object
Details:
  TestName: test_footer_card_box_attribute
  Description: This test is intended to verify that the 'box' attribute of the returned ui.Card object from the footer_card function is set to 'footer'.
Execution:
  Arrange: No setup is required as the function does not take any arguments.
  Act: Invoke the footer_card function and get the 'box' attribute of the returned ui.Card object.
  Assert: Check whether the 'box' attribute is equal to 'footer'.
Validation:
  This test is crucial as the box attribute needs to be set to 'footer' for the function to work as expected. This verifies that the function correctly sets the box attribute of the returned ui.Card object.

Scenario 3: Validate the caption attribute of the returned ui.Card object
Details:
  TestName: test_footer_card_caption_attribute
  Description: This test is intended to verify that the 'caption' attribute of the returned ui.Card object from the footer_card function is set to 'Made with 💛 and H2O Wave.'.
Execution:
  Arrange: No setup is required as the function does not take any arguments.
  Act: Invoke the footer_card function and get the 'caption' attribute of the returned ui.Card object.
  Assert: Check whether the 'caption' attribute is equal to 'Made with 💛 and H2O Wave.'.
Validation:
  This test is important as the caption attribute needs to be set to 'Made with 💛 and H2O Wave.' for the function to work as expected. This verifies that the function correctly sets the caption attribute of the returned ui.Card object.
```
"""

# ********RoostGPT********
import pytest
from cards import footer_card
from h2o_wave import ui

class Test_CardsFooterCard:

    def test_footer_card_return_type(self):
        card = footer_card()
        assert isinstance(card, ui.Card), "The returned object is not an instance of ui.Card"

    def test_footer_card_box_attribute(self):
        card = footer_card()
        assert card.box == 'footer', "The 'box' attribute of the returned ui.Card object is not set to 'footer'"

    def test_footer_card_caption_attribute(self):
        card = footer_card()
        assert card.caption == 'Made with 💛 and H2O Wave.', "The 'caption' attribute of the returned ui.Card object is not set to 'Made with 💛 and H2O Wave.'"
