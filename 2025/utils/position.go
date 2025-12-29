package utils

import "fmt"

type Position struct {
	X uint
	Y uint
}

func (r Position) InRange(v uint) bool {
	return r.X <= v && v <= r.Y
}

func Pos[V int | int8 | int16 | int32 | int64 | uint | uint8 | uint16 | uint32 | uint64](x, y V) Position {
	if x < 0 || y < 0 {
		panic(fmt.Sprintf("%v or %v < 0", x, y))
	}
	return Position{uint(x), uint(y)}
}
