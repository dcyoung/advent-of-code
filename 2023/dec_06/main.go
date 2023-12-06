package main

import (
	"fmt"
)

type Race struct {
	time   int
	record int
}

func (r *Race) woudlWin(waitTime int) bool {
	if waitTime > r.time-1 {
		return false
	}
	return waitTime*(r.time-waitTime) > r.record
}

func (r *Race) numWaysToWin() int {
	numWays := 0
	for i := 1; i < r.time; i++ {
		if r.woudlWin(i) {
			numWays++
		}
	}
	return numWays
}

func Parse(fpath string, combine bool) []Race {
	switch fpath {
	case "inputs/example.txt":
		if combine {
			return []Race{{71530, 940200}}
		}
		return []Race{
			{7, 9},
			{15, 40},
			{30, 200},
		}
	case "inputs/input.txt":
		if combine {
			return []Race{{62649190, 553101014731074}}
		}
		return []Race{
			{62, 553},
			{64, 1010},
			{91, 1473},
			{90, 1074},
		}
	default:
		panic("invalid fpath")
	}
}

func pt1(fpath string) {
	races := Parse(fpath, false)
	result := 1
	for _, r := range races {
		result *= r.numWaysToWin()
	}
	fmt.Println(result)
}

func pt2(fpath string) {
	races := Parse(fpath, true)
	result := 1
	for _, r := range races {
		result *= r.numWaysToWin()
	}
	fmt.Println(result)
}

func main() {

	// input.txt
	const fpath = "inputs/example.txt"
	// const fpath = "inputs/input.txt"
	pt1(fpath)
	pt2(fpath)
}
