package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"

	utils "example.com/common"
)

type CubeSet struct {
	Blue  int
	Red   int
	Green int
}
type Game struct {
	Id           int
	Observations []CubeSet
}

func parseObservation(s string) CubeSet {
	obs := CubeSet{}

	s = strings.TrimSpace(s)
	colorParts := strings.Split(s, ",")

	for _, colorPart := range colorParts {
		colorPart := strings.TrimSpace(colorPart)
		parts := strings.Split(colorPart, " ")
		count, err := strconv.Atoi(parts[0])
		utils.Check(err)
		switch strings.ToLower(parts[1]) {
		case "blue":
			obs.Blue = count
		case "red":
			obs.Red = count
		case "green":
			obs.Green = count
		default:
			panic("unknown color")
		}
	}

	return obs
}

func parseGame(s string) Game {
	parts := strings.Split(s, ":")

	// parse game ID
	gameId, err := strconv.Atoi(strings.TrimSpace(strings.TrimPrefix(parts[0], "Game")))
	utils.Check(err)

	// parse observations
	observations := []CubeSet{}
	if len(parts) > 1 {
		obsStrings := strings.Split(parts[1], ";")
		for _, obsString := range obsStrings {
			observations = append(observations, parseObservation(obsString))
		}
	}

	return Game{Id: gameId, Observations: observations}
}

func parseGames(fPath string) []Game {
	file, err := os.Open(fPath)
	utils.Check(err)
	defer file.Close()

	scanner := bufio.NewScanner(file)
	games := []Game{}
	for scanner.Scan() {
		s := scanner.Text()
		games = append(games, parseGame(s))
	}
	utils.Check(scanner.Err())
	return games
}

func isObservationPossible(obs CubeSet, reality CubeSet) bool {
	if obs.Blue > reality.Blue || obs.Red > reality.Red || obs.Green > reality.Green {
		return false
	}
	return true
}

func isGamePossible(game Game, reality CubeSet) bool {
	for _, obs := range game.Observations {
		if !isObservationPossible(obs, reality) {
			return false
		}
	}
	return true
}

func calcMinimumReality(observations []CubeSet) CubeSet {
	minimumReality := CubeSet{}
	for _, obs := range observations {
		if obs.Blue > minimumReality.Blue {
			minimumReality.Blue = obs.Blue
		}
		if obs.Red > minimumReality.Red {
			minimumReality.Red = obs.Red
		}
		if obs.Green > minimumReality.Green {
			minimumReality.Green = obs.Green
		}
	}
	return minimumReality
}

func pt1() {
	target := CubeSet{Blue: 14, Red: 12, Green: 13}
	games := parseGames("inputs/input.txt")
	possible := utils.Filter(games, func(item Game) bool {
		return isGamePossible(item, target)
	})

	total := 0
	for _, game := range possible {
		total += game.Id
	}
	fmt.Println(total)
}

func pt2() {
	games := parseGames("inputs/input.txt")
	total := 0
	for _, game := range games {
		minReality := calcMinimumReality(game.Observations)
		total += minReality.Blue * minReality.Red * minReality.Green
	}
	fmt.Println(total)
}

func main() {
	pt1()
	pt2()
}
