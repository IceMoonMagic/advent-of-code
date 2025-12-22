package utils

import (
	"fmt"
	"os"
)

func ReadFile(day int, filename string) string {
	content, err := os.ReadFile(fmt.Sprintf("day%d/%s", day, filename))
	if err != nil {
		panic(err)
	}
	return string(content)
}
