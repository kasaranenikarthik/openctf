package core

import (
	"errors"
	"io/ioutil"
	"os"

	"github.com/easyctf/openctf/structs"
	"gopkg.in/yaml.v2"
)

var (
	// sampleConfig
	sampleConfig = structs.Config{
		CTFName:     "OpenCTF",
		BindAddress: ":1600",
		Environment: "production",
		Database: structs.DatabaseConfig{
			Provider: "sqlite",
		},
	}

	// ErrorNoConfigFile is thrown when the file isn't there.
	ErrorNoConfigFile = errors.New("The configuration file is missing")
)

// ValidateConfig will validate your configuration based on rules.
func ValidateConfig(config structs.Config) error {
	return nil
}

// LoadConfigFile loads a configuration from the given file.
func LoadConfigFile(filename string) (config structs.Config, err error) {
	contents, err := ioutil.ReadFile(filename)
	if err != nil {
		if os.IsNotExist(err) {
			err = ErrorNoConfigFile
			return
		}
		return
	}
	config, err = LoadConfig(contents)
	ValidateConfig(config)
	return
}

// LoadConfig loads a configuration from the given bytearray.
func LoadConfig(contents []byte) (config structs.Config, err error) {
	err = yaml.Unmarshal(contents, &config)
	return
}

// WriteSampleConfig writes the sample configuration into the given file.
func WriteSampleConfig(filename string) (config structs.Config, err error) {
	contents, err := yaml.Marshal(&sampleConfig)
	if err != nil {
		return
	}
	ioutil.WriteFile(filename, []byte(contents), os.ModePerm)
	return sampleConfig, nil
}
