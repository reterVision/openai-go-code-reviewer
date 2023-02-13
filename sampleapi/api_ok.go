package sampleapi

import (
	"fmt"
	"sync"
)

// HelloWorld ...
func HelloWorld() {

	wg := sync.WaitGroup()
	wg.Add(1)
	go func() {
		defer wg.Done()
		fmt.Printf("test goroutine")
	}()
	wg.Wait()

	for i := 0; i < 10; i++ {
		for j := 0; j < 10; j++ {
			fmt.Printf("Hello, world!")
		}
	}

	for i := 0; i < 10; i++ {
		fmt.Printf("Test Output\n")
	}
}
