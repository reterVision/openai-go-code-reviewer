package sampleapi

var (
	buckets []entry
)

// hasSpace returns an index pair if buckets[a] or buckets[b] has space to insert one more new value
func hasSpace(indexes ...int) (int, int) {
	for _, index := range indexes {
		for i := range buckets[index] {
			if buckets[index][i] == "" {
				return index, i
			}
		}
	}
	return -1, -1
}
