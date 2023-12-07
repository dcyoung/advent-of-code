package main

import (
	"fmt"
	"sort"
	"strconv"
	"strings"

	utils "example.com/common"
)

type Card rune

const joker Card = 74

type DecomposedHand map[Card]int
type Hand struct {
	cards      []Card
	decomposed DecomposedHand
	priority   int
}

type Play struct {
	original string
	hand     Hand
	bid      int
}

func (decomposed *DecomposedHand) Priority() int {
	counts := []int{}

	for _, count := range *decomposed {
		counts = append(counts, count)
	}
	sort.SliceStable(counts, func(i, j int) bool {
		return counts[i] > counts[j]
	})

	// five of a kind
	if counts[0] == 5 {
		return 0
	}

	// four of a kind
	if counts[0] == 4 {
		return 1
	}

	// full house
	if counts[0] == 3 && counts[1] == 2 {
		return 2
	}

	// three of a kind
	if counts[0] == 3 {
		return 3
	}
	// two pair
	if counts[0] == 2 && counts[1] == 2 {
		return 4
	}
	// one pair
	if counts[0] == 2 {
		return 5
	}

	// high card
	return 6
}

func (h *Hand) Beats(other *Hand, cardOrder *[]Card) bool {
	if h.priority < other.priority {
		return true
	}
	if h.priority > other.priority {
		return false
	}
	for i, card := range h.cards {
		other := other.cards[i]
		strength := utils.IndexOf(*cardOrder, card)
		challengerStrength := utils.IndexOf(*cardOrder, other)
		if challengerStrength != strength {
			return strength < challengerStrength
		}
	}

	return true
}

func parse(fPath string, jokers bool) ([]string, []Play) {
	lines, err := utils.ParseLines(fPath)
	utils.Check(err)
	// ...
	plays := []Play{}
	for _, line := range lines {
		parts := strings.Split(line, " ")
		bid, err := strconv.Atoi(parts[1])
		utils.Check(err)
		cards := []Card(parts[0])

		decomposed := DecomposedHand{}
		for _, card := range cards {
			decomposed[card]++
		}

		if jokers {
			nJokers, ok := decomposed[joker]
			if ok {
				delete(decomposed, joker)
				k, _ := utils.MaxEntry(decomposed)
				decomposed[k] += nJokers
			}
		}

		plays = append(plays, Play{original: line, hand: Hand{
			cards:      cards,
			decomposed: decomposed,
			priority:   decomposed.Priority(),
		}, bid: bid})
	}
	return lines, plays
}

func pt1(fpath string) {
	_, plays := parse(fpath, false)

	cardOrder := []Card("AKQJT98765432")
	// sort plays
	// utils.PPrintLn(plays)
	sort.SliceStable(plays, func(i, j int) bool {
		v := plays[j].hand.Beats(&plays[i].hand, &cardOrder)
		return v
	})
	// utils.PPrintLn(plays)

	total := 0
	for i, play := range plays {
		// fmt.Println(play.original, play.hand.cards)
		rank := i + 1
		total += play.bid * rank
	}

	fmt.Println(total)
}

func pt2(fpath string) {
	_, plays := parse(fpath, true)

	cardOrder := []Card("AKQT98765432J")
	// sort plays
	// utils.PPrintLn(plays)
	sort.SliceStable(plays, func(i, j int) bool {
		v := plays[j].hand.Beats(&plays[i].hand, &cardOrder)
		return v
	})
	// utils.PPrintLn(plays)

	total := 0
	for i, play := range plays {
		// fmt.Println(play.original, play.hand.cards)
		rank := i + 1
		total += play.bid * rank
	}

	fmt.Println(total)
}

func main() {
	fmt.Println([]rune("J"))
	const fpath = "inputs/example.txt"
	// const fpath = "inputs/input.txt"
	pt1(fpath)
	pt2(fpath)
}
