package utils

import "strconv"

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
