package day3

import (
	"slices"
	"strconv"
	"strings"

	"github.com/icemoonmagic/advent-of-code/2025/utils"
)

func Main() uint {
	inputText := utils.ReadFile(3, "input.txt")
	inputBanks := parseInput(inputText)
	joltages := make([]uint, 0, len(inputBanks))
	for _, bank := range inputBanks {
		joltages = append(joltages, uint(maxOverJoltage(bank)))
	}
	return utils.Sum(joltages)
}

func parseInput(inputText string) [][]uint8 {
	lines := strings.Fields(inputText)
	banks := make([][]uint8, 0, len(lines))
	for _, line := range lines {
		bank := make([]uint8, 0, len(line))
		for _, nR := range line {
			nI, _ := strconv.Atoi(string(nR))
			bank = append(bank, uint8(nI))
		}
		banks = append(banks, bank)
	}
	return banks
}

func maxJoltage(bank []uint8) uint8 {
	if len(bank) == 2 {
		return bank[0]*10 + bank[1]
	} else if len(bank) < 2 {
		panic("<2")
	}

	current := maxJoltage(bank[1:])
	if bank[0] >= current/10 {
		l := current / 10
		r := current - (l * 10)
		if l > r {
			return bank[0]*10 + l
		} else {
			return bank[0]*10 + r
		}
	} else {
		return current
	}
}

func maxOverJoltage(bank []uint8) uint {
	return combine(_maxOverJoltage(bank, 12))
}

func _maxOverJoltage(bank []uint8, available uint8) []uint8 {
	if len(bank) == int(available) {
		return bank
	} else if available == 0 {
		return []uint8{}
	} else if len(bank) == 0 {
		panic("Bank Empty")
	}
	var maxE uint8
	var maxI int
	for i, e := range bank[:len(bank)-int(available)+1] {
		if maxE < e {
			maxE = e
			maxI = i
		}
	}
	return slices.Concat(
		[]uint8{maxE},
		_maxOverJoltage(bank[maxI+1:], available-1),
	)
}

func combine(inputs []uint8) uint {
	var total uint
	for _, n := range inputs {
		total = total*10 + uint(n)
	}
	return total
}
