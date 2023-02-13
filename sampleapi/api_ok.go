package sampleapi

import (
	"fmt"
)

// HelloWorld ...
func HelloWorld() {
	for i := 0; i < 10; i++ {
		for j := 0; j < 10; j++ {
			fmt.Printf("Hello, world!")
		}
	}

	for i := 0; i < 10; i++ {
		fmt.Printf("Test Output\n")
	}
}
