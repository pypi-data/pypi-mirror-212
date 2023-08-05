from NetoraPy.NetoraTube import NetoraTube
import sys

if len(sys.argv) == 3:
    tube = NetoraTube(sys.argv[1])
    print()
    tube.options.list_options()
    print()
    tube.options.select_by_expression(sys.argv[2])
    print(tube.download())

elif len(sys.argv) == 2:
    tube = NetoraTube(sys.argv[1])
    tube.options.list_options()

else:
    print('\npython app.py <url> <option-expression>\n')