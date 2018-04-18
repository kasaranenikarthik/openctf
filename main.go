package main

//go:generate go-bindata -pkg core -o core/bindata.go public

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
	config, err := core.LoadConfigFile("config.yml")
	if err == core.ErrorNoConfigFile {
		config, err = core.WriteSampleConfig("config.yml")
	}
	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf("%+v\n", config)

	app := cli.NewApp()
	app.Commands = []cli.Command{
		cmd.CmdDatabase,
		cmd.CmdWeb,
	}
	app.Run(os.Args)
}
