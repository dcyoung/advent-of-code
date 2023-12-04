package main

import (
	"fmt"
	"strconv"
	"strings"

	utils "example.com/common"
)

type Card struct {
	id             int
	numbers        []int
	winningNumbers []int
}

func parse(fPath string) ([]string, []Card) {
	lines, err := utils.ParseLines(fPath)
	utils.Check(err)

	cards := make([]Card, len(lines))
	for i, line := range lines {
		parts := strings.Split(line, ":")
		gameId, err := strconv.Atoi(strings.Fields(parts[0])[1])
		utils.Check(err)

		parts = strings.Split(parts[1], "|")
		winningNumbers := utils.MultiAtoi(strings.Fields(parts[0]))
		numbers := utils.MultiAtoi(strings.Fields(parts[1]))
		cards[i] = Card{gameId, numbers, winningNumbers}
	}

	return lines, cards
}

func (card *Card) nMatching() int {
	n := 0
	for _, i := range card.numbers {
		for _, j := range card.winningNumbers {
			if i == j {
				n++
				break
			}
		}
	}
	return n
}

func (card *Card) score() int {
	n := card.nMatching()
	if n == 0 {
		return 0
	}
	r := 1
	for i := 0; i < n-1; i++ {
		r *= 2
	}
	return r
}

func pt1(fpath string) {
	_, cards := parse(fpath)
	scores := make([]int, len(cards))
	for i, card := range cards {
		scores[i] = card.score()
	}
	total := utils.ISum(scores)
	fmt.Println(total)
}

func dfsScore(cardMatches *[]int, idx int) int {
	nWon := (*cardMatches)[idx]
	total := nWon
	for i := idx + 1; i < idx+1+nWon; i++ {
		total += dfsScore(cardMatches, i)
	}
	return total
}

func pt2(fpath string) {
	_, cards := parse(fpath)
	matches := make([]int, len(cards))
	for i, card := range cards {
		matches[i] = card.nMatching()
	}

	totalCards := len(cards)
	for i := range matches {
		totalCards += dfsScore(&matches, i)
	}

	fmt.Println(totalCards)
}

func main() {
	// const fpath = "inputs/example.txt"
	const fpath = "inputs/input.txt"
	pt1(fpath)
	pt2(fpath)
}
