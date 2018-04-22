package models

import (
	"github.com/easyctf/openctf/structs"
	"github.com/go-xorm/xorm"

	// sqlite driver
	_ "github.com/mattn/go-sqlite3"
)

var globEngine *xorm.Engine

// GetEngine returns a new xorm.Engine for the given config
func GetEngine(config structs.Config) (engine *xorm.Engine, err error) {
	globEngine, err = xorm.NewEngine(config.Database.Provider, config.Database.File)
	if err != nil {
		return nil, err
	}

	if err = globEngine.Sync(new(User)); err != nil {
		return nil, err
	}
	return globEngine, nil
}
