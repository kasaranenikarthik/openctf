package cmd

import (
	"github.com/urfave/cli"
)

// CmdDatabase is the subcommand for managing the database
var CmdDatabase = cli.Command{
	Name:  "db",
	Usage: "Subcommand for managing the database.",
	Subcommands: []cli.Command{
		{
			Name: "init",
		},
	},
}
