package utils

import "fmt"

type Position struct {
	X uint
	Y uint
}

func (pos Position) moved(x, y int) Position {
	return Pos(int(pos.X)+x, int(pos.Y)+x)
}

func Pos[V int | int8 | int16 | int32 | int64 | uint | uint8 | uint16 | uint32 | uint64](x, y V) Position {
	if x < 0 || y < 0 {
		panic(fmt.Sprintf("%v or %v < 0", x, y))
	}
	return Position{uint(x), uint(y)}
}
