package utils

import (
	"bufio"
	"bytes"
	"io"
	"os"
	"strings"
)

func ParseLines(fPath string) ([]string, error) {
	file, err := os.Open(fPath)
	Check(err)
	defer file.Close()
	scanner := bufio.NewScanner(file)
	lines := []string{}
	for scanner.Scan() {
		lines = append(lines, strings.TrimSpace(scanner.Text()))
	}
	return lines, scanner.Err()
}

func CountLines(r io.Reader) (int, error) {
	buf := make([]byte, 32*1024)
	count := 0
	lineSep := []byte{'\n'}

	for {
		c, err := r.Read(buf)
		count += bytes.Count(buf[:c], lineSep)

		switch {
		case err == io.EOF:
			return count, nil

		case err != nil:
			return count, err
		}
	}
}

func MaxCharPerLine(r io.Reader) (int, error) {
	scanner := bufio.NewScanner(r)
	result := 0
	for scanner.Scan() {
		s := strings.TrimSpace(scanner.Text())
		result = max(result, len(s))
	}
	return result, scanner.Err()
}
