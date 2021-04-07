# 动态规划

## 0-1背包

[leetcode 416](https://leetcode.com/problems/partition-equal-subset-sum/)

为了每个数`只用一次`，遍历dp的时候`从右向左`

## 凑钱币

[leetcode 322](https://leetcode.com/problems/coin-change/)

如果每个数可以用`无限次`，就`从左向右`遍历dp

## dp数组降维

[leetcode 516](https://leetcode.com/problems/longest-palindromic-subsequence/)

将二维dp数组降维成一维的思路：

[![661Qmj.png](https://s3.ax1x.com/2021/03/17/661Qmj.png)](https://imgtu.com/i/661Qmj)

## 抢劫问题

[leetcode 198](https://leetcode.com/problems/house-robber/)

状态转移方程：`f(i) = max(f(i-1), f(i-2)+nums[i])`

### 进阶：环形房间，最后一间和第一间相邻

[leetcode 213](https://leetcode.com/problems/house-robber-ii/)

如果是环形房间，就从左到右抢一次（不抢最右边的房间），再从右向左抢一次（不抢最左边的房间），两者取最大值

## 买卖股票

[leetcode 121](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/)

两个状态：buy和sell，表示`当天执行这个操作所获得的利润`

状态转移方程：`buy = max(buy, -prices[i])`, `sell = max(sell, prices[i]+buy)`

### 进阶：不限买卖次数

[leetcode 122](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-ii/)

不限购买次数，只要明天的价格比今天低，就在今天卖出

因为这里要比较i和i+1，可能丢掉最后一天，所以可以在prices的末尾加上一个-1，这样就能保证最后一天会被算进去

### 进阶2：最多买卖两次

[leetcode 123](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-iii/)

因为要买卖两次，所以有4个状态，第一次买时所获得的利润buy1， 第一次卖出后的利润sell1，以及buy2和sell2

状态转移方程：`buy1 = max(buy1, -prices[i])`, `sell1 = max(sell1, prices[i]+buy1)`，这和前面的一样

第二次：`buy2 = max(buy2, sell1-prices[i])`，`sell2 = max(sell2, prices[i]+buy2)`

### 进阶3：最多买卖k次

[leetcode 188](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-iv/)

与买卖两次的逻辑相同，只不过这时有`2*k`个状态，不能用固定的指针来表示，所以用两个长度为k的数组buy和sell，`buy[i]`和`sell[i]`分别表示第i次买入和第i次卖出的利润

### 进阶4：卖完需要等一天

[leetcode 309](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-cooldown/)

有6个状态，buy，sell，cooldown分别代表今天执行该操作所获得的利润，prev_buy，prev_sell，prev_cooldown分别代表上一次执行该操作获得的利润

所以每天有三种可能：

- 今天买入，有两种情况：上一次是等待日和不是等待日，所以`buy = max(buy, prev_cooldown-prices[i])`

- 今天卖出，上一次只能是买入，所以`sell = prev_buy + prices[i]`

- 今天等待，有两种情况：上一次卖出和上一次等待，所以`cooldown = max(prev_sell, prev_cooldown)`

## 扔鸡蛋

[leetcode 887](https://leetcode.com/problems/super-egg-drop/)

有两种动态规划的思路

- 1.dp[i][j]表示i个鸡蛋和j层楼需要的最少测试次数

分为本次鸡蛋碎和不碎两种情况，如果碎了，鸡蛋数减1，接下来要到j层以下去测试(`dp[i-1][j-1]`)，如果没碎，鸡蛋数不变，接下来j层到n层(`dp[i][n-j`)，二者之间要取最差的情况

所以`dp[i][j] = min{max(dp[i-1][j-1], dp[i][n-j]) | for 1<= j <= n}`，最后第n层需要的测试次数就是dp[k][n]

这种方法会超时，还需要进一步通过二分法优化

- 2.dp[i][j]表示i个鸡蛋测试j次最多能测出的楼层数

同样分为碎与不碎两种情况，如果碎了，鸡蛋数减1，本次用掉了一次次数，所以还能测试j-1次(`dp[i-1][j-1]`)，如果没碎，鸡蛋数不变，还是能测j-1次(`dp[i][j-1]`)，又因为本次测试了一层，所以还要加个1

所以`dp[i][j] = dp[i-1][j-1] + dp[i][j-1] + 1`，而dp[i][j]表示的是楼层数，所以当dp[i][j]超过给定的层数n时测试结束，此时的j就是所求的测试次数

## 戳气球

[leetcode 312](https://leetcode.com/problems/burst-balloons/)

令dp[i][j]表示戳破从i到j范围内所有气球能得到的最高分数（不包括i和j），最终的答案就是dp[0][n+1]

假设中间最后一个戳破的是k，那最后一次的分数就是`nums[i]*nums[k]*nums[j]`

所以戳破i到j之间气球的分数就等于先戳破i到k和k到j，最后戳破k得到的分数，即`dp[i][j] = max(dp[i][j], dp[i][k]+dp[k][j]+nums[i]*nums[k]*nums[j]`

注意遍历的方向是从左下到右上

# 双指针

## 最长回文子串

[leetcode 5](https://leetcode.com/problems/longest-palindromic-substring/)

关键在于首先要跳过所有的相等字符

## 接雨水

[leetcode 42](https://leetcode.com/problems/trapping-rain-water/)

从左右两侧遍历，高的那一侧一定能够接到矮的那一侧的雨水，所以找到矮的那一侧，并判断当前格子能否接到水

# 位运算

## 不用加减乘除做加法

[剑指offer 65](https://leetcode-cn.com/problems/bu-yong-jia-jian-cheng-chu-zuo-jia-fa-lcof/)

`a^b`是不进位时加法的结果，`(a&b)<<1`是进位，当进位为0时，计算结束

## 数组中有两个只出现一次的数，其余出现两次

[剑指offer 56-1](https://leetcode-cn.com/problems/shu-zu-zhong-shu-zi-chu-xian-de-ci-shu-lcof/)

基本原则：`A xor B xor A = B`

所以计算整个数组的异或，结果就是两个只出现一次的数字`A xor B`，假设`A xor B = C`

这时只需要找到一个`在C中为1`的位i（A和B的第i位一定是不同的），就可以将A和B区分开

在数组nums的所有n中，只要第i位是1的就去跟A异或，不是1的就跟B异或，就将问题拆分成了两组`数组中只有一个只出现一次的数`的问题

## 数组中有一只出现一次的数，其余出现三次

[剑指offer 56-2](https://leetcode-cn.com/problems/shu-zu-zhong-shu-zi-chu-xian-de-ci-shu-ii-lcof/)

统计32个数字位，每一个数字位对所有的n计算`与`，然后统计当前位是1的次数，如果那个单独的数字在第i位是0，那这个位计算与后结果为1的次数应该是`3的倍数`

# 贪心

## 割绳子

[剑指offer 14](https://leetcode-cn.com/problems/jian-sheng-zi-lcof/)

分割成1，结果是`1*(n-1)`

分割成2，结果是`2*(n-2)`，比1的情况`1*1*(n-2)`要好

分割成3，结果是`3*(n-3)`，比2的情况`1*2*(n-3)`要好

分割成3，结果是`4*(n-4)`，与分割乘2相同

分割成5，结果是`2*3*(n-5)`

分割成6，结果是`3*3*(n-6)`

所以得到最大值的方式是尽量分割成`3的倍数`
