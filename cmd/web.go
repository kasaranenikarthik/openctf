package cmd

import (
	"log"

	"github.com/easyctf/openctf/core"
	"github.com/urfave/cli"
)

// CmdWeb is the subcommand for starting the web server
var CmdWeb = cli.Command{
	Name:  "web",
	Usage: "Subcommand for starting the web server.",
	Flags: []cli.Flag{
		cli.StringFlag{
			Name:  "config",
			Usage: "Path to the configuration file.",
			Value: "config.yml",
		},
	},
	Action: func(c *cli.Context) {
		// Read the config
		config, err := core.LoadConfigFile(c.String("config"))
		if err != nil {
			log.Fatal(err)
		}

		// Run the server
		server, err := core.CreateServer(config)
		if err != nil {
			log.Fatal(err)
		}
		server.Start()
	},
}
