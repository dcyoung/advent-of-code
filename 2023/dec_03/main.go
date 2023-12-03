package main

import (
	"fmt"
	"strconv"
	"strings"

	utils "example.com/common"
)

const EMPTY_SYMBOLS = "."
const DIGIT_SYMBOLS = "0123456789"

type Span struct {
	y  int
	x1 int
	x2 int
}

type Point2D struct {
	y int
	x int
}

func calculateSpans(occupancyMask [][]bool) []Span {
	spans := []Span{}
	for y, row := range occupancyMask {
		prev := false
		for x, value := range row {
			if value {
				if !prev {
					spans = append(spans, Span{y: y, x1: x, x2: x})
				} else {
					spans[len(spans)-1].x2 = x
				}
			}
			prev = value
		}
	}
	return spans
}

func adjacent(s Span, p Point2D) bool {
	return p.y <= (s.y+1) && p.y >= (s.y-1) && p.x >= (s.x1-1) && p.x <= (s.x2+1)
}

func sum(arr []int) int {
	sum := 0
	for _, valueInt := range arr {
		sum += valueInt
	}
	return sum
}

func parseSchematic(fPath string) ([]string, []Point2D, []Span) {
	lines, err := utils.ParseLines(fPath)
	utils.Check(err)

	maskNumeric := utils.Make2D[bool](len(lines), len(lines[0]))
	markers := []Point2D{}
	for y, line := range lines {
		for x, char := range line {
			c := string(char)
			if strings.Contains(EMPTY_SYMBOLS, c) {
				continue
			}
			if strings.Contains(DIGIT_SYMBOLS, c) {
				maskNumeric[y][x] = true
			} else {
				markers = append(markers, Point2D{y, x})
			}
		}
	}
	spans := calculateSpans(maskNumeric)

	return lines, markers, spans
}

func parseNumber(s Span, lines []string) int {
	vStr := lines[s.y][s.x1 : s.x2+1]
	v, err := strconv.Atoi(vStr)
	utils.Check(err)
	return v
}

func pt1() {
	lines, markers, spans := parseSchematic("inputs/input.txt")
	spans = utils.Filter[Span](spans, func(s Span) bool {
		for _, m := range markers {
			if adjacent(s, m) {
				return true
			}
		}
		return false
	})

	numbers := []int{}
	for _, s := range spans {
		v := parseNumber(s, lines)
		numbers = append(numbers, v)
	}
	fmt.Println(sum(numbers))

}

func pt2() {
	lines, markers, spans := parseSchematic("inputs/input.txt")

	gearRatios := []int{}
	for _, m := range markers {
		numbers := []int{}
		for _, s := range spans {
			if adjacent(s, m) {
				v := parseNumber(s, lines)
				numbers = append(numbers, v)
			}
		}
		if len(numbers) == 2 {
			gearRatios = append(gearRatios, numbers[0]*numbers[1])
		}
	}

	fmt.Println(sum(gearRatios))
}

func main() {
	pt1()
	pt2()
}
