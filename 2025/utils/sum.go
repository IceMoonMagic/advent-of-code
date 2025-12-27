package utils

func Sum[V int | int8 | int16 | int32 | int64 | uint | uint8 | uint16 | uint32 | uint64 | float32 | float64](inputs []V) V {
	var total V
	for _, n := range inputs {
		total += n
	}
	return total
}
