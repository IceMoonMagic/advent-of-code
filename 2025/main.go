package main

import (
	"fmt"
	"os"
	"strconv"

	"github.com/icemoonmagic/advent-of-code/2025/day1"
	"github.com/icemoonmagic/advent-of-code/2025/day2"
	"github.com/icemoonmagic/advent-of-code/2025/day3"
)

func main() {
	var runDay = 1
	if len(os.Args) >= 2 {
		var err error
		if runDay, err = strconv.Atoi(os.Args[1]); err != nil {
			panic(err)
		}
	}
	fmt.Printf("Day %d\n", runDay)
	switch runDay {
	case 1:
		fmt.Println(day1.Main())
	case 2:
		fmt.Println(day2.Main())
	case 3:
		fmt.Println(day3.Main())
	default:
		fmt.Println("Not Implemented")
	}
}
