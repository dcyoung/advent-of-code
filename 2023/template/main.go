package main

import (
	"fmt"

	utils "example.com/common"
)

func parse(fPath string) []string {
	lines, err := utils.ParseLines(fPath)
	utils.Check(err)
	// ...

	return lines
}

func pt1(fpath string) {
	lines := parse(fpath)
	fmt.Println(len(lines))
}

func pt2(fpath string) {
	lines := parse(fpath)
	fmt.Println(len(lines))
}

func main() {
	const fpath = "inputs/example.txt"
	// const fpath = "inputs/input.txt"
	pt1(fpath)
	pt2(fpath)
}
