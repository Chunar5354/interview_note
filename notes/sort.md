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

### 直接插入排序

每一趟都把nums[i]向前插入到合适的位置，当遍历到最后一个元素时，数组有序

```go
func straightSort(nums []int) []int {
	for i := 1; i < len(nums); i++ {
		if nums[i] <= nums[i-1] {
			// 每当遇到一个数字n比它前一个数字大，就将所有比n大的数全部后移一位，把n插到前面
			temp := nums[i]
			j := i - 1
			for j > 0 && nums[j] > temp {
				nums[j+1] = nums[j]
				j--
			}
			nums[j+1] = temp
		}
	}
	return nums
}
```

### 希尔排序

将整个数组按照间隔k分组，逐渐减小k，每一趟将每个分组按照直接插入排序方法排序

它的优势在于每一趟排序后，整个数组的有序性大大提高，所以后面的操作中需要移动的数据量就会减少

```go
func shellSort(nums []int) []int {
	// 从len(nums)/2开始逐步缩小间隔
	for k := len(nums) / 2; k > 0; k /= 2 {
		// 从第k个元素开始，每一组进行直接插入排序
		for i := k; i < len(nums); i++ {
			if nums[i] < nums[i-k] {
				tmp := nums[i]
				j := i - k
				for j >= 0 && nums[j] > tmp {
					nums[j+k] = nums[j]
					j -= k
				}
				nums[j+k] = tmp
			}
		}
	}
	return nums
}
```

### 冒泡排序

每当找到nums[i] > nums[i-1]，就将二者交换，所以每次遍历之后最后一个元素就是数组的最大值

依次减小遍历的上限，就能够时整个数组有序

```go
func bubbleSort(nums []int) []int {
	for i := 0; i < len(nums)-1; i++ {
		for j := 0; j < len(nums)-i-1; j++ {
			if nums[j] > nums[j+1] {
				// 遇到相邻的数字前一个比后一个大，就交换
				nums[j], nums[j+1] = nums[j+1], nums[j]
			}
		}
	}
	return nums
}
```

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

### 简单选择排序

每次遍历找到整个数组的最小值，将它放在最前面

依次增大遍历的初始点，使得整个数组有序

```go
func simpleSelectSort(nums []int) []int {
	for i := 0; i < len(nums); i++ {
		curr := i
		// 每次选出后面的最小值与当前值nums[i]交换
		for j := i + 1; j < len(nums); j++ {
			if nums[j] < nums[curr] {
				curr = j
			}
		}
		nums[i], nums[curr] = nums[curr], nums[i]
	}
	return nums
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

### 归并排序

每次将数组从中间拆分成两部分，用分治的思想分别对这两部分进行归并排序，然后将两个有序的子数组按照顺序合并成一个数组

```go
func mergeSort(nums []int) []int {
	if len(nums) <= 1 {
		return nums
	}
	var tmp []int
	// 2路归并，将数组分成两部分，分别归并排序
	tmp = append(tmp, nums...)
	m := len(tmp) / 2
	t1 := mergeSort(tmp[:m])
	t2 := mergeSort(tmp[m:])
	var i, i1, i2 int
	// 将归并排序后的两个数组按顺序合并
	for i1 < len(t1) && i2 < len(t2) {
		if t1[i1] > t2[i2] {
			nums[i] = t2[i2]
			i2++
		} else {
			nums[i] = t1[i1]
			i1++
		}
		i++
	}

	if i1 < len(t1) {
		for i < len(nums) {
			nums[i] = t1[i1]
			i++
			i1++
		}
	}
	if i2 < len(t2) {
		for i < len(nums) {
			nums[i] = t2[i2]
			i++
			i2++
		}
	}
	return nums
}
```