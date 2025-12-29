package day4

import (
	"strings"

	"github.com/icemoonmagic/advent-of-code/2025/utils"
)

type position struct {
	x uint
	y uint
}

func Main() uint {
	inputText := utils.ReadFile(4, "input.txt")
	inputData := parseInput(inputText)
	var totalMoved uint
	for {
		moveable := findMoveableCells(inputData)
		if len(moveable) == 0 {
			return totalMoved
		}
		totalMoved += uint(len(moveable))
		clearCells(moveable, inputData)
	}
}

func parseInput(inputText string) [][]rune {
	lines := strings.Fields(inputText)
	data := make([][]rune, len(lines))
	for i, l := range lines {
		data[i] = []rune(l)
	}
	return data
}

func findAdjacent(pos, bound position) []position {
	var result = make([]position, 0, 8)
	u, d, l, r := 0 < pos.y, pos.y < bound.y-1, 0 < pos.x, pos.x < bound.x-1
	if u {
		if l {
			result = append(result, position{pos.x - 1, pos.y - 1})
		}
		result = append(result, position{pos.x, pos.y - 1})
		if r {
			result = append(result, position{pos.x + 1, pos.y - 1})
		}
	}
	if l {
		result = append(result, position{pos.x - 1, pos.y})
	}
	if r {
		result = append(result, position{pos.x + 1, pos.y})
	}
	if d {
		if l {
			result = append(result, position{pos.x - 1, pos.y + 1})
		}
		result = append(result, position{pos.x, pos.y + 1})
		if r {
			result = append(result, position{pos.x + 1, pos.y + 1})
		}
	}
	return result
}

func canMoveCell(pos, bound position, data [][]rune) bool {
	var count uint8
	for _, a := range findAdjacent(pos, bound) {
		if data[a.y][a.x] == '@' {
			count += 1
		}
		if count >= 4 {
			return false
		}
	}
	return true
}

func findMoveableCells(data [][]rune) []position {
	result := make([]position, 0, len(data)*len(data[0]))
	yBound := uint(len(data))
	for y, row := range data {
		bound := position{uint(len(row)), uint(yBound)}
		for x, cell := range row {
			if cell != '@' {
				continue
			}
			cellPos := position{uint(x), uint(y)}
			if canMoveCell(cellPos, bound, data) {
				result = append(result, cellPos)
			}
		}
	}
	return result
}

func clearCells(cells []position, data [][]rune) {
	for _, c := range cells {
		data[c.y][c.x] = '.'
	}
}
