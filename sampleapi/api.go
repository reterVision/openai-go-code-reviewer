package sampleapi

import (
	"fmt"
)

// DumbAPI ...
func DumbAPI(name string, age int) string {
	return fmt.Sprintf("Name: %s; Age: %d", name, age)
}
