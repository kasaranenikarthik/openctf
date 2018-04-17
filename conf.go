package main

import (
	"errors"
	"io/ioutil"
	"os"

	"gopkg.in/yaml.v2"
)

// Config describes the configuration for all of OpenCTF.
type Config struct {
	CTFName     string `yaml:"ctf-name"`
	BindAddress string `yaml:"bind-address"`
	Environment string `yaml:"environment"`
}

var (
	// sampleConfig
	sampleConfig = Config{
		"OpenCTF",
		":1600",
		"production",
	}

	// ErrorNoConfigFile is thrown when the file isn't there.
	ErrorNoConfigFile = errors.New("The configuration file is missing")
)

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
func WriteSampleConfig(filename string) (err error) {
	contents, err := yaml.Marshal(&sampleConfig)
	if err != nil {
		return err
	}
	ioutil.WriteFile(filename, []byte(contents), os.ModePerm)
	return nil
}
