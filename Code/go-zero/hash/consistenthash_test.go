package hash

import (
	"fmt"
	"strconv"
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/tal-tech/go-zero/core/mathx"
)

const (
	keySize     = 20
	requestSize = 1000
)

func BenchmarkConsistentHashGet(b *testing.B) {
	ch := NewConsistentHash()
	for i := 0; i < keySize; i++ {
		ch.Add("localhost:" + strconv.Itoa(i))
	}

	for i := 0; i < b.N; i++ {
		ch.Get(i)
	}
}

func TestConsistentHash(t *testing.T) {
	ch := NewCustomConsistentHash(0, nil)
	val, ok := ch.Get("any")
	assert.False(t, ok)
	assert.Nil(t, val)

	for i := 0; i < keySize; i++ {
		ch.AddWithReplicas("localhost:"+strconv.Itoa(i), minReplicas<<1)
	}

	keys := make(map[string]int)
	for i := 0; i < requestSize; i++ {
		key, ok := ch.Get(requestSize + i)
		assert.True(t, ok)
		keys[key.(string)]++
	}

	mi := make(map[interface{}]int, len(keys))
	for k, v := range keys {
		mi[k] = v
	}
	entropy := mathx.CalcEntropy(mi)
	assert.True(t, entropy > .95)
}

func TestConsistentHashIncrementalTransfer(t *testing.T) {
	prefix := "anything"
	create := func() *ConsistentHash {
		ch := NewConsistentHash()
		for i := 0; i < keySize; i++ {
			ch.Add(prefix + strconv.Itoa(i))
		}
		return ch
	}

	originCh := create()
	keys := make(map[int]string, requestSize)
	for i := 0; i < requestSize; i++ {
		key, ok := originCh.Get(requestSize + i)
		assert.True(t, ok)
		assert.NotNil(t, key)
		keys[i] = key.(string)
	}

	node := fmt.Sprintf("%s%d", prefix, keySize)
	for i := 0; i < 10; i++ {
		laterCh := create()
		laterCh.AddWithWeight(node, 10*(i+1))

		for j := 0; j < requestSize; j++ {
			key, ok := laterCh.Get(requestSize + j)
			assert.True(t, ok)
			assert.NotNil(t, key)
			value := key.(string)
			assert.True(t, value == keys[j] || value == node)
		}
	}
}
