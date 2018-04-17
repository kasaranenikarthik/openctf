package main

import (
	"fmt"
	"log"
)

func main() {
	// Configuration setup
	config, err := LoadConfigFile("config.yml")
	if err == ErrorNoConfigFile {
		err = WriteSampleConfig("config.yml")
	}
	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf("%+v\n", config)

	// Run the server
	server, err := CreateServer(config)
	if err != nil {
		log.Fatal(err)
	}
	server.Start()
}
