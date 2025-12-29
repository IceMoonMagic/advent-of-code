package day5

import (
	"slices"
	"strconv"
	"strings"

	"github.com/icemoonmagic/advent-of-code/2025/utils"
)

func Main(inputText string) uint {
	fresh, available := parseInput(inputText)
	var result = make([]uint, 0)
	for _, a := range available {
		if isFresh(a, fresh) {
			result = append(result, a)
		}
	}
	_ = result
	// return uint(len(result))
	return countFresh(fresh)
}

func parseInput(inputText string) ([]utils.Position, []uint) {
	fresh := make([]utils.Position, 0)
	available := make([]uint, 0)
	for line := range strings.FieldsSeq(inputText) {
		if strings.Contains(line, "-") {
			lowerUpper := strings.Split(line, "-")
			lower, _ := strconv.Atoi(lowerUpper[0])
			upper, _ := strconv.Atoi(lowerUpper[1])
			fresh = append(fresh, utils.Pos(lower, upper))
		} else {
			id, _ := strconv.Atoi(line)
			available = append(available, uint(id))
		}
	}
	return fresh, available
}

func isFresh(id uint, fresh []utils.Position) bool {
	for _, f := range fresh {
		if f.InRange(id) {
			return true
		}
	}
	return false
}

func countFresh(freshRanges []utils.Position) uint {
	simpleFreshRanges := simplifyRanges(freshRanges)
	return countRanges(simpleFreshRanges)
}

func simplifyRanges(freshRanges []utils.Position) []utils.Position {
	nonOverlapping := make([]utils.Position, 0)
	nonOverlapping = append(nonOverlapping, freshRanges[0])
	for _, fr := range freshRanges {
		lb := struct {
			found bool
			index int
		}{false, 0}
		ate := true
		rm := make([]int, 0, len(nonOverlapping))
		for i, no := range nonOverlapping {
			if no.InRange(fr.X) && no.InRange(fr.Y) {
				// fr Exists entirely within no
				ate = false
				break
			} else if fr.X > no.Y {
				// fr exists entirely above no
				continue
			} else if fr.InRange(no.X) && fr.InRange(no.Y) {
				// fr completely contains no
				rm = append(rm, i)
			} else if no.InRange(fr.X) {
				// fr starts within no
				lb.found = true
				lb.index = i
			} else if no.InRange(fr.Y) {
				// fr ends within no
				if lb.found {
					nonOverlapping[lb.index].Y = no.Y
					rm = append(rm, i)
				} else {
					nonOverlapping[i].X = fr.X
				}
				ate = false
				break
			} else if fr.Y < no.X {
				// fr exists entirely below no
				if lb.found {
					nonOverlapping[lb.index].Y = fr.Y
				} else {
					nonOverlapping = slices.Insert(nonOverlapping, i, fr)
				}
				ate = false
				break
			} else {
				panic("Unexpected Case")
			}
		}
		if ate {
			if lb.found {
				nonOverlapping[lb.index].Y = fr.Y
			} else {
				nonOverlapping = append(nonOverlapping, fr)
			}
		}
		for _, r := range slices.Backward(rm) {
			nonOverlapping = slices.Delete(nonOverlapping, r, r+1)
		}
	}
	return slices.Clip(nonOverlapping)
}

func countRanges(freshRanges []utils.Position) uint {
	var total uint = 0
	for _, fr := range freshRanges {
		total += fr.Y + 1 - fr.X
	}
	return total
}
