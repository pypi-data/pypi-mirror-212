from IPython import display
from ...custom_exception import CustomException
from ..data import (ONES, TENS, THOUSANDS)
from ...logger import logging
import sys


def convert_whole_number(number: int) -> str:
    try:
        if number == 0:
            return ""

        words = ""
        group_count = 0

        while number > 0:
            triplet = number % 1000
            if triplet > 0:
                triplet_words = []
                hundreds_digit = triplet // 100
                tens_digit = (triplet % 100) // 10
                ones_digit = triplet % 10

                if hundreds_digit > 0:
                    triplet_words.append(ONES[hundreds_digit] + " hundred")

                if tens_digit >= 2:
                    triplet_words.append(TENS[tens_digit])
                    if ones_digit > 0:
                        triplet_words.append(ONES[ones_digit])
                elif tens_digit == 1:
                    triplet_words.append(ONES[tens_digit * 10 + ones_digit])
                elif ones_digit > 0:
                    triplet_words.append(ONES[ones_digit])

                if group_count > 0:
                    triplet_words.append(THOUSANDS[group_count])

                words = " ".join(triplet_words) + " " + words

            number //= 1000
            group_count += 1

        return words.strip()
    except Exception as e:
        logging.error(f"Error occurred while converting number to words: {e}")
        raise CustomException(str(e))


def convert_decimal_number(decimal):
    try:
        words = ""
        for digit in decimal:
            if digit == "0":
                words += "zero "
            else:
                words += ONES[int(digit)] + " "

        return words.strip()
    except Exception as e:
        logging.error(f"Error occurred while converting number to words: {e}")
        raise CustomException(str(e))


def number_to_word(number) -> str:
    try:
        # if not isinstance(number, (int, float)):
        #     return number  # Return the original value if not a valid number

        if number == 0:
            return "zero"

        if number < 0:
            return "minus " + number_to_word(abs(number))

        number_str = str(number)
        if "." in number_str:
            whole_part, decimal_part = number_str.split(".")
            words = (
                number_to_word(int(whole_part))
                + " point "
                + convert_decimal_number(decimal_part)
            )
        else:
            words = convert_whole_number(int(number_str))

        return words
    except Exception as e:
        logging.error(f"Error occurred while converting number to words: {e}")
        raise CustomException(str(e))
