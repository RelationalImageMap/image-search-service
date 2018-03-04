package main

import (
	"bytes"
	"fmt"
	"io"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"os/exec"
)

func indexHandler(w http.ResponseWriter, r *http.Request) {
	io.WriteString(w, "Received")
	body, err := ioutil.ReadAll(r.Body)
	if err != nil {
		log.Printf("Error reading body: %v", err)
		http.Error(w, "can't read body", http.StatusBadRequest)
		return
	}
	cmd := exec.Command("python3", "./TwitterApi/searchTweets.py", string(body))
	cmdOutput := &bytes.Buffer{}
	cmd.Stdout = cmdOutput
	err = cmd.Run()
	if err != nil {
		os.Stderr.WriteString(err.Error())
	}
	fmt.Print(string(cmdOutput.Bytes()))
}

func main() {
	http.HandleFunc("/", indexHandler)
	http.ListenAndServe(":8080", nil)
}
