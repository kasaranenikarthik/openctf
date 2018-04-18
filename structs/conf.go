package structs

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

	Database DatabaseConfig `yaml:"database"`
	Cache    CacheConfig    `yaml:"cache"`
}
