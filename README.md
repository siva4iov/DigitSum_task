# Digit Sum

This code is solution for a task where you need to count the number of entries in each group based on Digit Sum of number.


I wrote two approaches to solve this task:
 1. __Manual calculate function__. Works slower, but calculations are accurate.
 2. __Normal approximation function__. Works pretty fast, but calculations are inaccurate. Should be used with large amount of ids.

 ## First approach
 
The first approach is trivial, It counts the digit sum for each number, then counts the number of such digit sums.

## Second approach

I noticed (and also googled) that with an increase in the number of id, as in the CLT, the distribution tends to normal:
![Different_ids](/misc/diff_ids.png)

So I wrote a function, that approximate distribution to normal and calculate num of entries using normal distribution density function.

### !
There are a few assumptions that mostly make the values ​​not so true.
As example:
* I calculate std as (max_group - mean)/3, in normal distribution 3*std includes 99.7 % of entries
* The distribution is still not normal and never will be, so there can be no completely accurate calculations.

### But 
This approach gives us a strong speed gain:

![Results](/misc/results.png)

# Conclusion
I think, with large amount of ids, There is a use of the second algorithm.