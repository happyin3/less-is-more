package hash

import (
	"fmt"
	"sort"
	"strconv"
	"sync"

	"github.com/tal-tech/go-zero/core/lang"
	"github.com/tal-tech/go-zero/core/mapping"
)

const (
	TopWeight   = 100
	minReplicas = 100
	prime       = 16777619
)

type (
	Func func(data []byte) uint64

	ConsistentHash struct {
		hashFunc Func
		replicas int
		keys     []uint64
		ring     map[uint64][]interface{}
		nodes    map[string]lang.PlaceholderType
		lock     sync.RWMutex
	}
)

// NewConsistentHash returns a ConsistentHash.
func NewConsistentHash() *ConsistentHash {
	return NewCustomConsistentHash(minReplicas, Hash)
}

// NewCustomConsistentHash returns a ConsistentHash with given replicas and hash func.
func NewCustomConsistentHash(replicas int, fn Func) *ConsistentHash {
	if replicas < minReplicas {
		replicas = minReplicas
	}

	if fn == nil {
		fn = Hash
	}

	return &ConsistentHash{
		hashFunc: fn,
		replicas: replicas,
		ring:     make(map[uint64][]interface{}),
		nodes:    make(map[string]lang.PlaceholderType),
	}
}

func (h *ConsistentHash) Add(node interface{}) {
	h.AddWithReplicas(node, h.replicas)
}

func (h *ConsistentHash) AddWithReplicas(node interface{}, replicas int) {
	h.Remove(node)

	if replicas > h.replicas {
		replicas = h.replicas
	}

	nodeRepr := repr(node)
	h.lock.Lock()
	defer h.lock.Unlock()
	h.addNode(nodeRepr)

	for i := 0; i < replicas; i++ {
		hash := h.hashFunc([]byte(nodeRepr + strconv.Itoa(i)))
		h.keys = append(h.keys, hash)
		h.ring[hash] = append(h.ring[hash], node)
	}

	sort.Slice(h.keys, func(i, j int) bool {
		return h.keys[i] < h.keys[j]
	})
}

func (h *ConsistentHash) AddWithWeight(node interface{}, weight int) {
	replicas := h.replicas * weight / TopWeight
	h.AddWithReplicas(node, replicas)
}

func (h *ConsistentHash) Get(v interface{}) (interface{}, bool) {
	h.lock.RLock()
	defer h.lock.RUnlock()

	if len(h.ring) == 0 {
		return nil, false
	}

	hash := h.hashFunc([]byte(repr(v)))
	index := sort.Search(len(h.keys), func(i int) bool {
		return h.keys[i] >= hash
	}) % len(h.keys)

	nodes := h.ring[h.keys[index]]
	switch len(nodes) {
	case 0:
		return nil, false
	case 1:
		return nodes[0], true
	default:
		innerIndex := h.hashFunc([]byte(innerRepr(v)))
		pos := int(innerIndex % uint64(len(nodes)))
		return nodes[pos], true
	}
}

func (h *ConsistentHash) Remove(node interface{}) {
	nodeRepr := repr(node)

	h.lock.Lock()
	defer h.lock.Unlock()

	if !h.containsNode(nodeRepr) {
		return
	}

	for i := 0; i < h.replicas; i++ {
		hash := h.hashFunc([]byte(nodeRepr + strconv.Itoa(i)))
		index := sort.Search(len(h.keys), func(i int) bool {
			return h.keys[i] >= hash
		})
		if index < len(h.keys) && h.keys[index] == hash {
			h.keys = append(h.keys[:index], h.keys[index+1:]...)
		}
		h.removeNode(nodeRepr)
	}
}

func (h *ConsistentHash) removeRingNode(hash uint64, nodeRepr string) {
	if nodes, ok := h.ring[hash]; ok {
		newNodes := nodes[:0]
		for _, x := range nodes {
			if repr(x) != nodeRepr {
				newNodes = append(newNodes, x)
			}
			if len(newNodes) > 0 {
				h.ring[hash] = newNodes
			} else {
				delete(h.ring, hash)
			}
		}
	}
}

func (h *ConsistentHash) addNode(nodeRepr string) {
	h.nodes[nodeRepr] = lang.Placeholder
}

func (h *ConsistentHash) containsNode(nodeRepr string) bool {
	_, ok := h.nodes[nodeRepr]
	return ok
}

func (h *ConsistentHash) removeNode(nodeRepr string) {
	delete(h.nodes, nodeRepr)
}

func innerRepr(node interface{}) string {
	return fmt.Sprintf("%d:%v", prime, node)
}

func repr(node interface{}) string {
	return mapping.Repr(node)
}