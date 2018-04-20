package main

//go:generate go-bindata -pkg core -o core/bindata.go generated

import (
	"fmt"
	"log"
	"os"

	"github.com/easyctf/openctf/cmd"
	"github.com/easyctf/openctf/core"
	"github.com/urfave/cli"
)

func main() {
	// Configuration setup
	_, err := core.LoadConfigFile("config.yml")
	if err == core.ErrorNoConfigFile {
		fmt.Println("No config file found, one has been generated for you.")
		_, err = core.WriteSampleConfig("config.yml")
		return
	}
	if err != nil {
		log.Fatal(err)
	}

	app := cli.NewApp()
	app.Commands = []cli.Command{
		cmd.CmdDatabase,
		cmd.CmdWeb,
	}
	app.Run(os.Args)
}
