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

func getDay(day int) (func(string) uint, bool) {
	days := map[int]func(string) uint{
		1: day1.Main,
		2: day2.Main,
		3: day3.Main,
		4: day4.Main,
	}
	f, ok := days[day]
	return f, ok
}

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
	dayF, ok := getDay(runDay)
	if !ok {
		fmt.Println("Not Implemented")
		return
	}
	inputText := utils.ReadFile(runDay, sourceFile)
	fmt.Println(dayF(inputText))
}
