package main

import (
	"fmt"
	"os"
	"strconv"
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
	default:
		fmt.Println("Not Implemented")
	}
}
