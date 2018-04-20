package cmd

import (
	"log"

	"github.com/easyctf/openctf/structs"

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
		cli.StringFlag{
			Name:  "bind",
			Usage: "Bind address (overrides config.yml)",
		},
		cli.BoolFlag{
			Name:  "no-frontend",
			Usage: "Don't serve the static frontend.",
		},
	},
	Action: func(c *cli.Context) {
		// Read the config
		config, err := core.LoadConfigFile(c.String("config"))
		if err != nil {
			log.Fatal(err)
		}

		// Environmental options
		options := structs.WebserverOptions{
			NoFrontend:  c.Bool("no-frontend"),
			BindAddress: c.String("bind"),
		}
		config = config.Merge(options)

		// Run the server
		server, err := core.CreateServer(config)
		if err != nil {
			log.Fatal(err)
		}
		server.Start()
	},
}
