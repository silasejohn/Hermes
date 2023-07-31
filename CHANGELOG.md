
# Change Log
All notable changes to this project will be documented in this file.
 
The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [0.6.0] - 2023-07-31
Simple MQTT Client Update

### Added 
- New Hermes Class ~> implements a simple MQTT client capable of connecting to any broker given a hostname and port num. 
- independent logging across different files
- example implementation of hermes client in example.py

### Changed
- updated requirements.txt, config.ini files

## [0.5.0] - 2023-07-31
QoL Updates, setup for MQTT interceptor script

### Added 
- refined test script into example.py (organization and modularization of responsibilities)
- methods to grab logging threshold as strings or integer
- logic behind how and where a LOGGING_METHOD is defined

### Changed
- updated config and log directory paths to avoid clutter

### Removed
- unnecessary print statements, transitioned fully over to logging


## [0.4.0] - 2023-07-27
Parsing Module Poseidon

### Added 
- Created a parser module to read .ini setup files
- capable of displaying all available sections
- capable of pulling regular string input and boolean input
- capable of identifying if specific values are in a config file

## [0.3.0] - 2023-07-27
Logging Module Aristotle

### Changed
- Upgraded the Logging Module Aristotle:
- (1) Functionality for Console or/and File Logging
- (2) Restructuring of the Logging Utility to a Class (to manage multiple Logger Objects, Handlers, and Formatters)
- (3) Fluid Options for setting Logging Thresholds
- (4) Better Control on creation of Log Events
- (5) Pre-Defined Log Events for restarts, cleanses, formatting, etc.

## [0.2.0] - 2023-07-24
Creation of a simple CLI test utility to find an IP Address given an input hostname

### Added

- test.py simple program includes local environment variable storage, utility class, wrapper methods, string formatting, CLI argument options and parsing, custom exit codes, and comprehensive logging)

## [0.1.0] - 2023-07-24
  
Fundamental Project Setup + Config
 
### Added

- Install and Upgrade System Modules (frozen in requirements.txt)
- Create rudimentary README and CHANGELOG, .gitignore & LICENSE, .env files

## [Unreleased] - yyyy-mm-dd
- Working towards basic functionality of the CLI tool.
 
*future project features and functionality go here*
 
### Added
 
### Changed

### Deprecated

### Removed
 
### Fixed

### Security
- [Example Hyperlink Title](url.link.here)
  Description of Link to Resource
