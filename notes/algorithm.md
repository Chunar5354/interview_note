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

与买卖两次的逻辑相同，只不过这时有`2*k`个状态，不能用固定的指针来表示，所以用两个长度为k的数组buy和profit，`buy[i]`和`profit[i]`分别表示第i次买入和第i次卖出的利润

### 进阶4：卖完需要等一天

[leetcode 309](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-cooldown/)

有6个状态，buy，sell，cooldown分别代表今天执行该操作所获得的利润，prev_buy，prev_sell，prev_cooldown分别代表上一次执行该操作获得的利润

所以每天有三种可能：

- 今天买入，有两种情况：上一次是等待日和不是等待日，所以`buy = max(buy, prev_cooldown-prices[i])`

- 今天卖出，上一次只能是买入，所以`sell = prev_buy + prices[i]`

- 今天等待，有两种情况：上一次卖出和上一次等待，所以`cooldown = max(prev_sell, prev_cooldown)`

# 双指针

## 最长回文子串

[leetcode 5](https://leetcode.com/problems/longest-palindromic-substring/)

关键在于首先要跳过所有的相等字符
