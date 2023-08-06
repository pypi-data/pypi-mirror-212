# from MT_PerformanceLogging.LP import PerformanceLogger
from LogPerformance import  PerformanceLogger

import time
# Create an instance of PerformanceLogger
logger = PerformanceLogger(__name__)

# Use the logger to measure function performance
@logger.log_performance
def my_function():
    num=int(input('Enter Num value:'))
    result=0
    power=1
    for x in str(num):
        y=int(x)
        result= result + y**power
        power=power+1
    if num==result:
        print(f'The provide {num} is Disarum')
    else:
        print(f'The Provided {num} is Not a Disarum Number')
   
    time.sleep(1)

# Call the function
my_function()
