package models

import (
	"github.com/easyctf/openctf/structs"
	"github.com/go-xorm/xorm"

	// sqlite driver
	_ "github.com/mattn/go-sqlite3"
)

// GetEngine returns a new xorm.Engine for the given config
func GetEngine(config structs.Config) (engine *xorm.Engine, err error) {
	engine, err = xorm.NewEngine(config.Database.Provider, config.Database.File)
	return
}
