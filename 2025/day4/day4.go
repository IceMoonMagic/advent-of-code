package day4

import (
	"strings"

	"github.com/icemoonmagic/advent-of-code/2025/utils"
)

func Main(inputText string) uint {
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

func findAdjacent(pos, bound utils.Position) []utils.Position {
	var result = make([]utils.Position, 0, 8)
	u, d, l, r := 0 < pos.Y, pos.Y < bound.Y-1, 0 < pos.X, pos.X < bound.X-1
	if u {
		if l {
			result = append(result, utils.Pos(pos.X-1, pos.Y-1))
		}
		result = append(result, utils.Pos(pos.X, pos.Y-1))
		if r {
			result = append(result, utils.Pos(pos.X+1, pos.Y-1))
		}
	}
	if l {
		result = append(result, utils.Pos(pos.X-1, pos.Y))
	}
	if r {
		result = append(result, utils.Pos(pos.X+1, pos.Y))
	}
	if d {
		if l {
			result = append(result, utils.Pos(pos.X-1, pos.Y+1))
		}
		result = append(result, utils.Pos(pos.X, pos.Y+1))
		if r {
			result = append(result, utils.Pos(pos.X+1, pos.Y+1))
		}
	}
	return result
}

func canMoveCell(pos, bound utils.Position, data [][]rune) bool {
	var count uint8
	for _, a := range findAdjacent(pos, bound) {
		if data[a.Y][a.X] == '@' {
			count += 1
		}
		if count >= 4 {
			return false
		}
	}
	return true
}

func findMoveableCells(data [][]rune) []utils.Position {
	result := make([]utils.Position, 0, len(data)*len(data[0]))
	yBound := len(data)
	for y, row := range data {
		bound := utils.Pos(len(row), yBound)
		for x, cell := range row {
			if cell != '@' {
				continue
			}
			cellPos := utils.Pos(x, y)
			if canMoveCell(cellPos, bound, data) {
				result = append(result, cellPos)
			}
		}
	}
	return result
}

func clearCells(cells []utils.Position, data [][]rune) {
	for _, c := range cells {
		data[c.Y][c.X] = '.'
	}
}
