# Source global definitions

if [ -f /etc/bashrc ]; then
	. /etc/bashrc
fi

# Uncomment the following line if you don't like systemctl's auto-paging feature:
# export SYSTEMD_PAGER=
# User specific aliases and functions

# Include ~/bin in the PATH
PATH=$PATH:~/bin

###################################################
# Display container's welcome message / help 
###################################################
cat /etc/motd
