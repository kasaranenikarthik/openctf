package structs

import (
	"errors"
	"fmt"
)

// DatabaseConfig describes the database configuration for OpenCTF.
type DatabaseConfig struct {
	Provider string `yaml:"provider"`
	File     string `yaml:"file"`
	Host     string `yaml:"host"`
	Port     string `yaml:"port"`
	Username string `yaml:"username"`
	Password string `yaml:"password"`
}

// CacheConfig describe the cache configuration (if any) for OpenCTF.
type CacheConfig struct {
	Enabled bool `yaml:"enabled"`
}

// Config describes the configuration for all of OpenCTF.
type Config struct {
	CTFName     string `yaml:"ctf-name"`
	BindAddress string `yaml:"bind-address"`
	Environment string `yaml:"environment"`

	Database   DatabaseConfig `yaml:"database"`
	Cache      CacheConfig    `yaml:"cache"`
	NoFrontend bool           `yaml:"-"`
}

// Merge adds WebserverOptions to the config
func (c Config) Merge(w WebserverOptions) Config {
	c.NoFrontend = w.NoFrontend
	if w.BindAddress != "" {
		c.BindAddress = w.BindAddress
	}
	return c
}

// GetDSN constructs a DSN out of the database configuration
func (c DatabaseConfig) GetDSN() (string, error) {
	switch c.Provider {
	case "sqlite3":
		if c.File == "" {
			return "", errors.New("empty 'file' field is invalid for provider sqlite3")
		}
		return fmt.Sprintf("sqlite:/%s", c.File), nil
	default:
		return "", fmt.Errorf("'%s' is not a valid database provider", c.Provider)
	}
}
