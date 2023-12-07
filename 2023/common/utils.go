package utils

import (
	"strconv"
	"strings"

	"github.com/k0kubun/pp"
)

func Check(e error) {
	if e != nil {
		panic(e)
	}
}

func Filter[T any](items []T, fn func(item T) bool) []T {
	filteredItems := []T{}
	for _, value := range items {
		if fn(value) {
			filteredItems = append(filteredItems, value)
		}
	}
	return filteredItems
}

func ISum(arr []int) int {
	sum := 0
	for _, valueInt := range arr {
		sum += valueInt
	}
	return sum
}

func MultiAtoi(arr []string) []int {
	result := make([]int, len(arr))
	for i, value := range arr {
		result[i], _ = strconv.Atoi(value)
	}
	return result
}

func ParseListOfInts(s string) []int {
	s = strings.TrimSpace(s)
	return MultiAtoi(strings.Split(s, " "))
}

func IndexOf[T comparable](arr []T, value T) int {
	for i, v := range arr {
		if v == value {
			return i
		}
	}
	return -1
}

func MaxEntry[T comparable](m map[T]int) (T, int) {
	var maxKey T
	var maxValue int
	for key, value := range m {
		if value > maxValue {
			maxKey = key
			maxValue = value
		}
	}
	return maxKey, maxValue
}

func PPrintLn[T any](x T) {
	pp.Println(x)
}

func MinMax(array []int) (int, int) {
	var max int = array[0]
	var min int = array[0]
	for _, value := range array {
		if max < value {
			max = value
		}
		if min > value {
			min = value
		}
	}
	return min, max
}

func ChunkSlice(slice []int, chunkSize int) [][]int {
	var chunks [][]int
	for i := 0; i < len(slice); i += chunkSize {
		end := i + chunkSize

		// necessary check to avoid slicing beyond
		// slice capacity
		if end > len(slice) {
			end = len(slice)
		}

		chunks = append(chunks, slice[i:end])
	}

	return chunks
}
