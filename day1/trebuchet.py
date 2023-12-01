import re

WORD_TO_DIGIT = {
  'one': '1',
  'two': '2',
  'three': '3',
  'four': '4',
  'five': '5',
  'six': '6',
  'seven': '7',
  'eight': '8',
  'nine': '9'
}

def first_last_digit(number: str) -> int:
    return int(number[0] + number[-1])

def extract_digits(input: str) -> str:
    # need to make use of lookahead to avoid clashes of twone as 21 and not as 2
    # Regex matches any digit or keys from the dict.
    digits = re.findall(rf'(?=(\d|{"|".join(WORD_TO_DIGIT.keys())}))', input.rstrip())
    # replace words with dict values
    return "".join([digit if digit.isnumeric() else WORD_TO_DIGIT[digit] for digit in digits])

if __name__ ==  '__main__':
    with open('day1/input.txt', 'r') as f:
        # first extract the digits and then take the first and last digit
        lines = [first_last_digit(number) for number in [extract_digits(line) for line in f]]

    print(sum(lines))