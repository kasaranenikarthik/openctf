package core

import (
	"errors"
	"io/ioutil"
	"os"

	"gopkg.in/yaml.v2"
)

// DatabaseConfig describes the database configuration for OpenCTF.
type DatabaseConfig struct {
	Provider string `yaml:"provider"`
}

// Config describes the configuration for all of OpenCTF.
type Config struct {
	CTFName     string `yaml:"ctf-name"`
	BindAddress string `yaml:"bind-address"`
	Environment string `yaml:"environment"`

	Database DatabaseConfig `yaml:"database"`
}

var (
	// sampleConfig
	sampleConfig = Config{
		CTFName:     "OpenCTF",
		BindAddress: ":1600",
		Environment: "production",
		Database: DatabaseConfig{
			Provider: "sqlite",
		},
	}

	// ErrorNoConfigFile is thrown when the file isn't there.
	ErrorNoConfigFile = errors.New("The configuration file is missing")
)

// ReadConfig reads from the config file based on cmd-line arguments.
func ReadConfig() (config Config, err error) {
	return LoadConfigFile("config.yml")
}

// LoadConfigFile loads a configuration from the given file.
func LoadConfigFile(filename string) (config Config, err error) {
	contents, err := ioutil.ReadFile(filename)
	if err != nil {
		if os.IsNotExist(err) {
			err = ErrorNoConfigFile
			return
		}
		return
	}
	config, err = LoadConfig(contents)
	return
}

// LoadConfig loads a configuration from the given bytearray.
func LoadConfig(contents []byte) (config Config, err error) {
	err = yaml.Unmarshal(contents, &config)
	return
}

// WriteSampleConfig writes the sample configuration into the given file.
func WriteSampleConfig(filename string) (config Config, err error) {
	contents, err := yaml.Marshal(&sampleConfig)
	if err != nil {
		return
	}
	ioutil.WriteFile(filename, []byte(contents), os.ModePerm)
	return sampleConfig, nil
}
