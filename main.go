package main

import (
	"flag"
	"fmt"
	"log"

	"github.com/thehowl/conf"
)

// VERSION is the current version of OpenCTF, will be injected by the build script on release builds.
var VERSION = "dev"

func main() {
	confFile := flag.String("conf", "openctf.conf", "Location of the config file (will be created if it doesn't exist).")
	flag.Parse()

	if *confFile == "" {
		fmt.Println("Config file required. See -h for more details.")
		return
	}

	c := Config{}
	err := conf.Load(&c, *confFile)
	if err == conf.ErrNoFile {
		conf.Export(defaultConfig, *confFile)
		fmt.Printf("The default configuration has been written to '%s'. Please modify this file and rerun the application.\n", *confFile)
		return
	}
	if err != nil {
		log.Fatal(err)
	}

	app := OpenCTF{c}
	app.Run()
}
