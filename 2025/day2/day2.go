package day2

import (
	"slices"
	"strconv"
	"strings"

	"github.com/icemoonmagic/advent-of-code/2025/utils"
)

func Main() uint {
	inputText := strings.TrimSpace(utils.ReadFile(2, "input.txt"))
	inputRanges := parseInput(inputText)
	invalidIds := []uint{}
	for _, ir := range inputRanges {
		invalidIds = slices.Concat(invalidIds, scanRange(ir))
	}
	sum := uint(0)
	for _, invId := range invalidIds {
		sum += invId
	}
	return sum
}

func parseInput(input string) [][]uint {
	rangeStrings := strings.Split(input, ",")
	ranges := make([][]uint, 0, len(rangeStrings))
	for _, _range := range rangeStrings {
		lowerUpper := strings.Split(_range, "-")
		lower, _ := strconv.Atoi(lowerUpper[0])
		upper, _ := strconv.Atoi(lowerUpper[1])
		ranges = append(ranges, []uint{uint(lower), uint(upper)})
	}
	return ranges
}

func scanRange(lowerUpper []uint) []uint {
	result := []uint{}
	for i := lowerUpper[0]; i <= lowerUpper[1]; i += 1 {
		n := strconv.FormatUint(uint64(i), 10)
		/* [Toggle]
		if len(n)%2 != 0 {
			continue
		}

		l := n[:len(n)/2]
		r := n[len(n)/2:]

		if l == r {
			result = append(result, i)
		}
		/*/
		for j := 1; j <= len(n)/2; j += 1 {
			if len(n)%j != 0 {
				continue
			}
			fragment := n[:j]
			if n == strings.Repeat(fragment, len(n)/j) {
				result = append(result, i)
				break
			}
		}

		//  */
	}
	return result
}
