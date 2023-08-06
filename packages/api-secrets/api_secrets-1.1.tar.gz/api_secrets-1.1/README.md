This program was developed as a wrapper to the keyring module. It was specifically developed to:
	- provide a JSON structure for storing objects beyond just a password
	- get around the windows maximum storage size for secrets by fracturing them (up to 10 "fragments")
