package main

import (
	"fmt"
	"sort"
	"strings"

	utils "example.com/common"
)

type RangeInclusive struct {
	a int
	b int
}

func (m RangeInclusive) InRange(v int) bool {
	return v >= m.a && v <= m.b
}

func (m RangeInclusive) Convert(other RangeInclusive, v int) int {
	if !m.InRange(v) {
		return v
	}
	return other.a + (v - m.a)
}

type MappedRange struct {
	src RangeInclusive
	dst RangeInclusive
}

func (r MappedRange) Src2Dst(v int) int {
	return r.src.Convert(r.dst, v)
}

func (r MappedRange) Dst2Src(v int) int {
	return r.dst.Convert(r.src, v)
}

type CATEGORY struct {
	value int
	name  string
}
type Map struct {
	src      CATEGORY
	dst      CATEGORY
	mappings []MappedRange
}

func (m Map) Src2Dst(v int) int {
	prev := v
	for _, r := range m.mappings {
		v = r.Src2Dst(v)
		if v != prev {
			return v
		}
		prev = v
	}
	return v
}

func (m Map) Dst2Src(v int) int {
	prev := v
	for _, r := range m.mappings {
		v = r.Dst2Src(v)
		if v != prev {
			return v
		}
		prev = v
	}
	return v
}

func parseMappedRange(s string) MappedRange {
	parts := utils.ParseListOfInts(s)
	dstA := parts[0]
	n := parts[2]
	srcA := parts[1]
	return MappedRange{
		src: RangeInclusive{a: srcA, b: srcA + n - 1},
		dst: RangeInclusive{a: dstA, b: dstA + n - 1},
	}
}

func parseMappings(mappingLines []string) []MappedRange {
	mappings := []MappedRange{}
	for _, line := range mappingLines {
		mappings = append(mappings, parseMappedRange(line))
	}
	return mappings
}

type RuleSet struct {
	seeds         []int
	maps          []Map
	categories    []CATEGORY
	locationCache []map[int]int
	seedCache     []map[int]int
}

type SpanNode struct {
	span     *RangeInclusive
	children []*SpanNode
}

func (n *SpanNode) AddChild(child *SpanNode) {
	n.children = append(n.children, child)
}

func (r *RangeInclusive) Intersection(other *RangeInclusive) (RangeInclusive, error) {
	v := RangeInclusive{
		a: max(r.a, other.a),
		b: min(r.b, other.b),
	}
	if v.a > v.b {
		return v, fmt.Errorf("no intersection")
	}
	return v, nil
}

func (n *SpanNode) AddChildren(mappings []MappedRange) {
	sort.Slice(mappings, func(i, j int) bool {
		return mappings[i].src.a < mappings[j].src.a
	})
	a := n.span.a

	for _, m := range mappings {
		if a > n.span.b {
			return
		}
		if m.src.a > n.span.b || m.src.b < a {
			continue
		}

		if m.src.a > a {
			// flat map the preceeding empty space, then take the intersection
			n.AddChild(&SpanNode{span: &RangeInclusive{
				a: a,
				b: m.src.a - 1,
			}, children: []*SpanNode{}})
		}
		// take the intersection
		overlap, err := n.span.Intersection(&m.src)
		utils.Check(err)
		n.AddChild(&SpanNode{span: &overlap, children: []*SpanNode{}})

		a = overlap.b + 1
	}

	// flat map any remaining space
	if a <= n.span.b {
		// flat map the preceeding empty space, then take the intersection
		n.AddChild(&SpanNode{span: &RangeInclusive{
			a: a,
			b: n.span.b,
		}, children: []*SpanNode{}})
	}
}

func parse(fPath string) ([]string, RuleSet) {
	lines, err := utils.ParseLines(fPath)
	utils.Check(err)

	seeds := utils.ParseListOfInts(strings.Split(lines[0], ":")[1])

	mappingGroups := [][]string{}
	for _, line := range lines[1:] {
		if strings.TrimSpace(line) == "" {
			continue
		}
		if strings.Contains(line, ":") {
			mappingGroups = append(mappingGroups, []string{})
		} else {
			if len(mappingGroups) == 0 {
				mappingGroups = append(mappingGroups, []string{line})
			} else {
				mappingGroups[len(mappingGroups)-1] = append(mappingGroups[len(mappingGroups)-1], line)
			}
		}
	}

	categories := []CATEGORY{
		{0, "seed"},
		{1, "soil"},
		{2, "fertilizer"},
		{3, "water"},
		{4, "light"},
		{5, "temperature"},
		{6, "humidity"},
		{7, "location"},
	}

	maps := make([]Map, len(mappingGroups))
	for i, mappingGroup := range mappingGroups {
		maps[i] = Map{
			src:      categories[i],
			dst:      categories[i+1],
			mappings: parseMappings(mappingGroup),
		}
	}

	// utils.PPrintLn(maps)
	locationCache := make([]map[int]int, len(maps))
	for i := range locationCache {
		locationCache[i] = make(map[int]int)
	}
	seedCache := make([]map[int]int, len(maps))
	for i := range seedCache {
		seedCache[i] = make(map[int]int)
	}
	return lines, RuleSet{
		seeds:         seeds,
		maps:          maps,
		categories:    categories,
		locationCache: locationCache,
		seedCache:     seedCache,
	}
}

func (r RuleSet) GetLocation(mapSrcV int, mapIdx int) int {
	if v, ok := r.locationCache[mapIdx][mapSrcV]; ok {
		return v
	}
	m := r.maps[mapIdx]
	v := m.Src2Dst(mapSrcV)
	if m.dst.name != "location" {
		v = r.GetLocation(v, mapIdx+1)
	}
	r.locationCache[mapIdx][mapSrcV] = v
	return v
}

func (r RuleSet) GetSeed(mapDstV int, mapIdx int) int {
	if v, ok := r.seedCache[mapIdx][mapDstV]; ok {
		return v
	}
	m := r.maps[mapIdx]
	v := m.Dst2Src(mapDstV)
	if m.src.name != "seed" {
		v = r.GetSeed(v, mapIdx-1)
	}
	r.seedCache[mapIdx][mapDstV] = v
	return v
}

func pt1(fpath string) {
	_, rules := parse(fpath)
	// find lowest location w/ seed

	minLoc := int(^uint(0) >> 1)
	for _, seed := range rules.seeds {
		if loc := rules.GetLocation(seed, 0); loc < minLoc {
			minLoc = loc
		}
	}

	fmt.Println(minLoc)
}

type MultiRange []RangeInclusive

func (m MultiRange) Contains(v int) bool {
	for _, r := range m {
		if r.InRange(v) {
			return true
		}
	}
	return false
}

func pt2(fpath string) {
	lines, rules := parse(fpath)
	values := utils.ParseListOfInts(strings.Split(lines[0], ":")[1])

	seedRanges := MultiRange{}
	i := 0
	for i < len(values) {
		a := values[i]
		n := values[i+1]
		seedRanges = append(seedRanges, RangeInclusive{a: a, b: a + n - 1})
		i += 2
	}
	sort.Slice(seedRanges, func(i2, j int) bool {
		return seedRanges[i2].a < seedRanges[j].a
	})

	nMaps := len(rules.maps)
	for loc := 0; loc < 99999999999; loc++ {
		if s := rules.GetSeed(loc, nMaps-1); seedRanges.Contains(s) {
			fmt.Println(loc)
			return
		}
	}
}

func main() {
	const fpath = "inputs/example.txt"
	// const fpath = "inputs/input.txt"
	pt1(fpath)
	pt2(fpath)
}
