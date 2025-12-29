package main

import (
	"fmt"
	"os"
	"strconv"

	"github.com/icemoonmagic/advent-of-code/2025/day1"
	"github.com/icemoonmagic/advent-of-code/2025/day2"
	"github.com/icemoonmagic/advent-of-code/2025/day3"
	"github.com/icemoonmagic/advent-of-code/2025/day4"
	"github.com/icemoonmagic/advent-of-code/2025/utils"
)

func main() {
	var runDay = 1
	var sourceFile = "input.txt"
	if len(os.Args) >= 2 {
		var err error
		if runDay, err = strconv.Atoi(os.Args[1]); err != nil {
			panic(err)
		}
		if len(os.Args) >= 3 {
			sourceFile = os.Args[2]
		}
	}
	fmt.Printf("Day %d, %s\n", runDay, sourceFile)
	inputText := utils.ReadFile(runDay, sourceFile)
	switch runDay {
	case 1:
		fmt.Println(day1.Main(inputText))
	case 2:
		fmt.Println(day2.Main(inputText))
	case 3:
		fmt.Println(day3.Main(inputText))
	case 4:
		fmt.Println(day4.Main(inputText))
	default:
		fmt.Println("Not Implemented")
	}
}
