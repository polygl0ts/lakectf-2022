package main

import (
	"bufio"
	"fmt"
	"os"

	"github.com/redpwn/pow"
)

func main() {
	c := pow.GenerateChallenge(5000)
	print(c)
	fmt.Printf("proof of work: curl -sSfL https://pwn.red/pow | sh -s %s\nsolution: ", c)
	s, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	if good, err := c.Check(s); err == nil && good {
		fmt.Println("good")
	} else {
		fmt.Println("bad")
	}
}
