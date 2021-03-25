## 常见排序算法

|  算法       | 时间复杂度  | 稳定性  |
|  ---------- | ---------  | -----  |
| 直接插入排序 | O(n^2)     | 稳定    |
| 希尔排序    | O(n*log(n)) ~ O(n^1.5) | 不稳定  |
| 冒泡排序    | O(n^2)     | 稳定    |
| 快速排序    | O(n*log(n)) ~ O(n^2) | 不稳定    |
| 简单选择排序 | O(n^2)     | 不稳定  |
| 堆排序      | O(n*log(n)) | 不稳定  |
| 归并排序    | O(n*log(n)) | 稳定   |

归并排序的空间复杂度是`O(n)`

可以看出，不稳定的算法大多是由`交换不相邻的元素`引起的


## 部分算法代码实现

### 快速排序

核心思想是分治法，令枢轴左边都小于枢轴，右边都大于枢轴，然后再对左右两部分进行排序

当含有相等的元素时，可以使枢轴部分变成一个区间`[lo, hi]`

```go
func quick_sort(nums []int, lo, hi int) []int {
	if lo >= hi {
		return nums
	}
	p1, p2, nums := sort(nums, lo, hi)
	nums = quick_sort(nums, lo, p1-1)
	nums = quick_sort(nums, p2+1, hi)
	return nums
}

func sort(nums []int, lo, hi int) (int, int, []int) {
	pivot := nums[lo]
	i := lo + 1
	// lo是枢轴，lo左边的要小于枢轴，hi右边的要大于枢轴
	// 最终lo和hi中间(闭区间)都等于枢轴
	for i <= hi {
		if nums[i] < pivot {
			nums[i], nums[lo] = nums[lo], nums[i]
			i++
			lo++
		} else if nums[i] > pivot {
			nums[i], nums[hi] = nums[hi], nums[i]
			hi--
		} else {
			i++
		}
		// fmt.Println(lo, hi, i, nums)
	}
	return lo, hi, nums
}
```

### 堆排序

核心思想是将数组看成一个`完全二叉树`，节点nums[n]的子节点是nums[2*n]和nums[2*n+1]

核心操作是`上浮`和`下沉`

要进行堆排序，首先要将数组`初始化`为一个堆


```go
func insert(nums []int, key int) []int {
	nums = append(nums, key)
	nums = swim(nums)
	return nums
}

// 上浮
func swim(nums []int) []int {
	n := len(nums) - 1
	for n > 1 {
		if nums[n] > nums[n/2] {
			nums[n], nums[n/2] = nums[n/2], nums[n]
		}
		n /= 2
	}
	return nums
}

func delMax(nums []int) (int, []int) {
	maxNum := nums[1]
	nums[1] = nums[len(nums)-1]
	nums[len(nums)-1] = 0
	nums = sink(nums, 1, len(nums)-1)
	return maxNum, nums
}

// 下沉
func sink(nums []int, k, n int) []int {
	for k*2 <= n {
		j := k * 2
		// 把2*k和2*k+1中更大的那个换到父结点上去
		if j < n && nums[j] < nums[j+1] {
			j++
		}
		// 如果已经满足了父结点大于子节点，下沉结束
		if nums[k] > nums[j] {
			return nums
		}
		nums[k], nums[j] = nums[j], nums[k]
		k = j
		fmt.Println(nums)
	}
	return nums
}

func sort(nums []int) []int {
	n := len(nums) - 1
	// 首先将数组初始化为一个堆
	for k := n / 2; k >= 1; k-- {
		nums = sink(nums, k, n)
	}
	// 每次将最大值取出，再对剩下的部分排序
	for n > 1 {
		nums[1], nums[n] = nums[n], nums[1]
		n--
		nums = sink(nums, 1, n)
	}
	return nums
}
```