package day1

import (
	"strconv"
	"strings"

	"github.com/icemoonmagic/advent-of-code/2025/utils"
)

func Main() uint {
	input := utils.ReadFile(1, "input.txt")

	return calculateCodeV2(strings.Fields(input))

}

func calculateCodeV1(sequence []string) uint {
	var count uint = 0
	var position int = 50
	for _, step := range sequence {
		position = (position + parseStep(step)) % 100
		if position == 0 {
			count += 1
		}
	}
	return count
}

func calculateCodeV2(sequence []string) uint {
	var count uint = 0
	var position int = 50
	for _, step := range sequence {
		change := parseStep(step)
		landed := position + change
		position = (landed%100 + 100) % 100

		if landed == 0 {
			count += 1
		} else if landed > 0 {
			count += uint(landed / 100)
		} else {
			count += uint(-landed / 100)
			if landed != change {
				count += 1
			}
		}
	}
	return count
}

func parseStep(step string) int {
	positive := step[0] == 'R'
	amount, err := strconv.Atoi(step[1:])
	if err != nil {
		panic(err)
	}

	if positive {
		return amount
	} else {
		return -amount
	}
}
