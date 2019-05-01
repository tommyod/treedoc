 #!/bin/sh
 
 # ==============================================================================
 # LINTING
 # This script will check spelling conventions
 # Run it by typing $ bash ./linting.sh
 # ==============================================================================


function invgrep () {
    # grep with inverse exist status
    # grep "$@" -> Run grep with the parameters
    grep "$@" 
    # $((! $?))-> $? fetches the last exit code, ! reverts it
    return $((! $?))
}

words="sub-package sub-module sub- super-"
# Iterate the string variable using for loop
for word in $words; do
    echo "Searching for word: '$word'"
    echo "----------------------------------"
    invgrep "$word" -r -n '--include=*.'{py,md,txt} 
done