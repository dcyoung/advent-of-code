package main

import (
	"bufio"
	"fmt"
	"os"
	"sort"
	"strconv"
	"strings"

	utils "example.com/common"
)

type Result struct {
	Sub string
	Dig int
	Idx int
}

func pt1() {
	file, err := os.Open("input.txt")
	utils.Check(err)
	defer file.Close()

	scanner := bufio.NewScanner(file)
	total := 0
	for scanner.Scan() {
		s := scanner.Text()

		digits := []rune{}
		for _, r := range s {
			if r <= 57 {
				digits = append(digits, r)
			}
		}
		vAsStr := string([]rune{digits[0], digits[len(digits)-1]})
		v, err := strconv.Atoi(vAsStr)
		utils.Check(err)
		total += v
	}
	utils.Check(scanner.Err())

	fmt.Println(total)
}

func pt2() {
	file, err := os.Open("input.txt")
	utils.Check(err)
	defer file.Close()

	scanner := bufio.NewScanner(file)
	total := 0
	for scanner.Scan() {
		s := scanner.Text()
		results := []Result{}
		for dig, sub := range []string{"zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"} {
			if firstIdx := strings.Index(s, sub); firstIdx >= 0 {
				results = append(results, Result{sub, dig, firstIdx})
				if lastIdx := strings.LastIndex(s, sub); lastIdx != firstIdx {
					results = append(results, Result{sub, dig, lastIdx})
				}
			}
			if firstIdx := strings.Index(s, fmt.Sprint(dig)); firstIdx >= 0 {
				results = append(results, Result{fmt.Sprint(dig), dig, firstIdx})
				if lastIdx := strings.LastIndex(s, fmt.Sprint(dig)); lastIdx != firstIdx {
					results = append(results, Result{fmt.Sprint(dig), dig, lastIdx})
				}
			}
		}
		sort.SliceStable(results, func(i, j int) bool {
			return results[i].Idx <= results[j].Idx
		})
		vAsStr := fmt.Sprint(results[0].Dig) + fmt.Sprint(results[len(results)-1].Dig)
		v, err := strconv.Atoi(vAsStr)
		utils.Check(err)
		total += v
	}
	utils.Check(scanner.Err())

	fmt.Println(total)
}

func main() {
	pt1()
	pt2()
}
