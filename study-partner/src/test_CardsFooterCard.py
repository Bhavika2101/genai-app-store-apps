# ********RoostGPT********
"""
Test generated by RoostGPT for test python-unit-studypartner using AI Type Open AI and AI Model gpt-4

ROOST_METHOD_HASH=footer_card_062d99a4b9
ROOST_METHOD_SIG_HASH=footer_card_3e136a9ae6

```
Scenario 1: Validate the box value in the footer_card function
Details:
  TestName: test_footer_card_box_value
  Description: This test is intended to verify if the 'box' value of the footer card returned by the function is 'footer'.
Execution:
  Arrange: No arrangement necessary as no parameters are passed to the function.
  Act: Invoke the footer_card function and store the returned footer_card object.
  Assert: Check if the 'box' attribute of the returned footer_card object is equal to 'footer'.
Validation:
  Rationalize: The 'box' attribute is crucial for the correct positioning of the footer card on the UI. This test ensures that the footer card always appears at the correct location.

Scenario 2: Validate the caption value in the footer_card function
Details:
  TestName: test_footer_card_caption_value
  Description: This test is intended to verify if the 'caption' value of the footer card returned by the function is 'Made with 💛 and H2O Wave.'.
Execution:
  Arrange: No arrangement necessary as no parameters are passed to the function.
  Act: Invoke the footer_card function and store the returned footer_card object.
  Assert: Check if the 'caption' attribute of the returned footer_card object is equal to 'Made with 💛 and H2O Wave.'.
Validation:
  Rationalize: The 'caption' attribute is essential for displaying the correct message on the footer card. This test ensures that the footer card always shows the correct message.

Scenario 3: Validate the type of the returned object from the footer_card function
Details:
  TestName: test_footer_card_return_type
  Description: This test is intended to verify if the object returned by the footer_card function is of type ui.footer_card.
Execution:
  Arrange: No arrangement necessary as no parameters are passed to the function.
  Act: Invoke the footer_card function and store the returned object.
  Assert: Check if the type of the returned object is ui.footer_card.
Validation:
  Rationalize: Ensuring the type of the returned object is crucial to avoid type errors when using the object. This test ensures that the function always returns an object of the correct type.
```
"""

# ********RoostGPT********
import os
from h2o_wave import ui, Q, data
from cards import footer_card
import pytest

class Test_CardsFooterCard:

    @pytest.mark.regression
    def test_footer_card_box_value(self):
        # Act
        returned_card = footer_card()
        # Assert
        assert returned_card.box == 'footer', 'Footer card box value does not match expected value "footer"'

    @pytest.mark.regression
    def test_footer_card_caption_value(self):
        # Act
        returned_card = footer_card()
        # Assert
        assert returned_card.caption == 'Made with 💛 and H2O Wave.', 'Footer card caption value does not match expected value "Made with 💛 and H2O Wave."'

    @pytest.mark.regression
    def test_footer_card_return_type(self):
        # Act
        returned_card = footer_card()
        # Assert
        assert isinstance(returned_card, ui.footer_card), 'Returned object is not of type ui.footer_card'
