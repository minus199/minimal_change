'''
Usage: 
    python3 coins.py \
        -d fifty_shekel:50 ten_shekel:10 five_shekel:5 shekel:1 half_shekel:0.5 quarter_shekel:0.25 agora:0.01 \
        -n ILS -a 1234.455 -s ₪
'''

from sanity_tester import sanity_test
from menu_builder import parse_input_args
from coins import compute_change

def main():
    context = parse_input_args()
    segments = compute_change(**context)
    sanity_test(segments=segments, **context)


if __name__ == '__main__':
    main()
