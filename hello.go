package main

import (
	"fmt"

	"openai-go-code-reviewer/sampleapi"
)

func main() {
	message := sampleapi.DumbAPI("test endpoint", 28)
	fmt.Println(message)
}
