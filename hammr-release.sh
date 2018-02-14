#!/bin/bash
# What is doing this script ?
# This script is automating stuff we use to do by hand to release Hammr
# He's performing in the first place some checks (run inside build-env, not existing directories, existing uforge-python-sdk version ...) to run correctly
# Then displaying a welcome message with the resume of what has been passed as arguments and some agreements regarding what he is doing and what you
# should do if he fails.

#Used to write bold in terminal to enforce some terms
bold=$(tput bold)
normal=$(tput sgr0)
boldify () {
  echo ${bold}${1}${normal}
}

#Describe how to use the tool
usage () {
  echo "Usage : "
  echo "hammr-release -b <remote_branch> -v <hammr_version> [-p <python_sdk_version>]"
  echo "    -b ) The remote branch to use for building hammr"
  echo "    -v ) The hammr version to release"
  echo "    -p ) The python_sdk_version to use for building hammr, by default using the same version as hammr"
  echo " Example for a 3.8.1 RC release : hammr-release -b master -v 3.8.1-RC1 -p 3.8.1-RC1"
  echo " Example for an official release : hammr-release -b master -v 3.8.1 -p 3.8.1"
  exit 1
}

#Get steps
get_step () {
  case ${1} in
    1) echo "::::::::::: First step : upload to Pypi the new Hammr $HAMMR_VERSION artifact";;
    2) echo "::::::::::: Second step : commit the changes in Hammr repository";;
    3) echo "::::::::::: Third step : create a github annotated tag $HAMMR_VERSION for the release";;
    4) echo "::::::::::: Fourth step : commit in Hammr repository a new setup.py version with uforge-python-sdk>=$HAMMR_VERSION";;
    5) echo "::::::::::: Fifth step : create a pull request to merge the release branch inside the master";;
  esac
}

#Clean working directory
clean_directory () {
  if [ -d  $WORKING_DIRECTORY ]; then
    echo "Cleaning the working directory ... "
    rm -rf $WORKING_DIRECTORY
  fi
}

#In case of failure, display remaining steps
steps_remaining () {
  if [ "$STEP_COMPLETED" -ge "1" ] && [ "$STEP_COMPLETED" -ne "$NB_STEPS" ]; then
    echo "Please visit $WORKING_DIRECTORY to see the repository state and perform by hand the following steps : "
    FROM=$((STEP_COMPLETED + 1))
    TO=$((NB_STEPS))
    for (( i=$FROM; i<=$TO; i++ ))
    do
      RESULT=$(get_step $i)
      echo $RESULT
    done
  fi
}

#Error in the release process
release_failed () {
  echo "  ______ _____  _____   ____  _____   "
  echo " |  ____|  __ \|  __ \ / __ \|  __ \  "
  echo " | |__  | |__) | |__) | |  | | |__) | "
  echo " |  __| |  _  /|  _  /| |  | |  _  /  "
  echo " | |____| | \ \| | \ \| |__| | | \ \  "
  echo " |______|_|  \_\_|  \_\\\____/|_|  \_\ "
  echo ""
  echo "Hammr release $HAMMR_VERSION failed"
  echo "${1}"
  steps_remaining
  exit 1
}

#Get the return status of the latest command and print an error if needed
verify_latest_command () {
  if [ $? -ne 0 ]; then
    release_failed "${1}"
  fi
}

#Add modified files in the stage and committed with the given message.
#Finally pushed to the specified branch
commit_and_push_changes () {
  FILES="setup.py hammr/utils/constants.py"
  git add $FILES
  verify_latest_command "Cannot add $FILES in the stage for commit"
  git commit -m "${1}"
  verify_latest_command "Cannot commit $FILES"
  git push origin $HAMMR_RELEASE_BRANCH
  verify_latest_command "Cannot push the changes on the remote server"
}

#Manage steps, variable used to specify which steps are remaining if there is a failure
STEP_COMPLETED=0
step_completed () {
  STEP_COMPLETED=${1}
  echo ""
  echo ""
  echo ""
  echo "   _____                      _      _           _ "
  echo "  / ____|                    | |    | |         | |"
  echo " | |     ___  _ __ ___  _ __ | | ___| |_ ___  __| |"
  echo " | |    / _ \| '_ \` _ \| '_ \| |/ _ \ __/ _ \/ _\` |"
  echo " | |___| (_) | | | | | | |_) | |  __/ ||  __/ (_| |"
  echo "  \_____\___/|_| |_| |_| .__/|_|\___|\__\___|\__,_|"
  echo "                       | |                         "
  echo "                       |_|                         "
  echo ""
}

#Display which step is running
display_running_step () {
  STEP_TO_COMPLETE=$(($STEP_COMPLETED + 1))
  RESULT=$(get_step $STEP_TO_COMPLETE)
  echo "$RESULT running ..."
}

#Display terminated string
terminated () {
  echo ""
  echo "#######################################################"
  echo " _____                   _             _           _ "
  echo "|_   _|__ _ __ _ __ ___ (_)_ __   __ _| |_ ___  __| |"
  echo "  | |/ _ \ '__| '_ \` _ \| | '_ \ / _\` | __/ _ \/ _\` |"
  echo "  | |  __/ |  | | | | | | | | | | (_| | ||  __/ (_| |"
  echo "  |_|\___|_|  |_| |_| |_|_|_| |_|\__,_|\__\___|\__,_|"
  echo ""
  echo "#######################################################"
  echo ""
}

# trap ctrl-c and call ctrl_c()
trap ctrl_c INT
function ctrl_c() {
  echo ""
  echo "Exiting by user CTRL-C"
  steps_remaining
  exit 1
}

#Parsing arguments
while getopts :b:v:p: options; do
   case $options in
      b) GIT_BASE_BRANCH=${OPTARG} ;;
      v) HAMMR_VERSION=${OPTARG} ;;
      p) SDK_VERSION=${OPTARG} ;;
      \?) printf "illegal option: -%s\n" "$OPTARG" >&2
       usage
       ;;
   esac
done
shift $(($OPTIND - 1))

#Setting sdk version with hammr version if not specified by the user
if [ ! "$SDK_VERSION" ]; then
    SDK_VERSION=$HAMMR_VERSION
fi

#Setting the directory used for the release and Hammr url
WORKING_DIRECTORY="/home/hammr-release-$HAMMR_VERSION"
HAMMR_REPO="usharesoft/hammr"
GIT_ADDRESS="https://github.com"
GIT_API_ADDRESS="https://api.github.com"
NB_STEPS=5
HAMMR_RELEASE_BRANCH="release-$HAMMR_VERSION"

#Verifying pre-requisite
#Mandatory arguments
if [ ! "$HAMMR_VERSION" ] || [ ! "$GIT_BASE_BRANCH" ]; then
    usage
fi
#Must be inside build env
if [ $HOME != "/home/ussrelease" ]; then
  release_failed "The release script automation must be executed inside build-env container"
fi
#Must have a file with pypi credentials
if [ ! -f "/home/ussrelease/.pypirc" ]; then
  release_failed "The PyPI UShareSoft credentials file shoud be present in /home/ussrelease/.pypirc"
fi
#Must not be inside git repo
if [ -d ".git" ]; then
  release_failed "The release script automation must not be executed inside a git repository"
fi
#The directory used for release must not exists on the filesystem
if [ -d "$WORKING_DIRECTORY" ]; then
  release_failed "The directory \""$WORKING_DIRECTORY"\", used for the release, must not exists on the filesystem"
fi
# Verify uforge-python-sdk version is available on Pypi
PYPI_URL="https://pypi.python.org/pypi"
STATUS=$(curl -o /dev/null --silent --head --write-out '%{http_code}' "$PYPI_URL/uforge_python_sdk/$SDK_VERSION")
if [ $STATUS -ne 200 ]; then
  release_failed "uforge_python_sdk $SDK_VERSION is not available on $PYPI_URL"
fi
#Verify hammr version we are releasing is not on Pypi
STATUS=$(curl -o /dev/null --silent --head --write-out '%{http_code}' "$PYPI_URL/hammr/$HAMMR_VERSION")
if [ $STATUS -eq 200 ]; then
  release_failed "hammr $HAMMR_VERSION is already available on $PYPI_URL"
fi

#Welcome message
HAMMR_VERSION_BOLD=$(boldify "$HAMMR_VERSION")
GIT_BASE_BRANCH_BOLD=$(boldify "$GIT_BASE_BRANCH")
SDK_VERSION_BOLD=$(boldify "$SDK_VERSION")

echo ""
echo "#############################################"
echo " __          __  _                          "
echo " \ \        / / | |                         "
echo "  \ \  /\  / /__| | ___ ___  _ __ ___   ___ "
echo "   \ \/  \/ / _ \ |/ __/ _ \| '_ \` _ \ / _ \\"
echo "    \  /\  /  __/ | (_| (_) | | | | | |  __/"
echo "     \/  \/ \___|_|\___\___/|_| |_| |_|\___|"
echo ""
echo "#############################################"
echo ""
echo "Hammr release version : $HAMMR_VERSION_BOLD"
echo "Hammr remote branch : $GIT_BASE_BRANCH_BOLD"
echo "uforge-python-sdk version : $SDK_VERSION_BOLD"
echo "working directory : $WORKING_DIRECTORY"
echo ""
echo ""
echo "This release is composed of $NB_STEPS steps that should complete successfully."
echo ""
for (( i=1; i<=$NB_STEPS; i++ ))
do
  RESULT=$(get_step $i)
  echo $RESULT
done
echo ""
echo "If one step is completed but not the others, you should complete by hand the process to remain in a stable state."
echo ""

#Ask for agreement to perform the release
echo "Do you really want to build Hammr $HAMMR_VERSION_BOLD from branch $GIT_BASE_BRANCH_BOLD (on repo $GIT_ADDRESS/$HAMMR_REPO) with uforge-python-sdk $SDK_VERSION_BOLD ? Y/n"
read AGREE
if [ -n "$AGREE" ]; then
  if [ "$AGREE" != "y" ] && [ "$AGREE" != "Y" ]; then
    echo "Release abandonned"
    exit 1
  fi
fi

display_running_step

#Clone hammr with only the branch specified by the user
git clone $GIT_ADDRESS/$HAMMR_REPO --branch $GIT_BASE_BRANCH --single-branch $WORKING_DIRECTORY
verify_latest_command "Cannot clone hammr repository"

#Move inside workspace
cd $WORKING_DIRECTORY
verify_latest_command "Cannot change directory, maybe an issue with $WORKING_DIRECTORY creation ... "

#Create a new branch because push on master are prohibited ... so we are doing it inside a branch and then merge it inside master
git checkout -b $HAMMR_RELEASE_BRANCH
verify_latest_command "Cannot checkout branch"

#Now we change the version of Hammr and SDK
sed -i "s/'uforge_python_sdk.*'/'uforge_python_sdk==$SDK_VERSION'/g" setup.py
sed -i "s/VERSION=.*/VERSION=\"$HAMMR_VERSION\"/g" ./hammr/utils/constants.py

# Then we build and push the artifact to Pypi
python setup.py clean bdist_wheel sdist bdist_egg bdist_wininst --plat-name=win32
verify_latest_command "Cannot build hammr artifact ... "


#Upload on pypi
twine upload -r pypi dist/*
if [ $? -ne 0 ]; then
  release_failed "Cannot upload hammr artifact ... "
fi

step_completed 1
display_running_step

#Finally, we can commit what we have done
#need to create a branch for PR, cannot push in master
commit_and_push_changes "Hammr release new version $HAMMR_VERSION"

step_completed 2
display_running_step

#Then we create a tag and push it to the server
git tag -a "$HAMMR_VERSION" -m "Hammr release new version $HAMMR_VERSION"
git push origin "$HAMMR_VERSION"

step_completed 3
display_running_step

#ie : we are using >= to enable the CI in github to work with .dev packages for pull request
sed -i "s/'uforge_python_sdk.*'/'uforge_python_sdk>=$SDK_VERSION'/g" setup.py
commit_and_push_changes "Hammr release $HAMMR_VERSION done, prepare next version."

step_completed 4
display_running_step

#Final step the pull request
echo "Username for $GIT_API_ADDRESS :"
read USERNAME
STATUS=$(curl -o /dev/null --silent --write-out '%{http_code}' --user "$USERNAME" --request POST --data '{"title":"Hammr release new version '$HAMMR_VERSION'","body":"Hammr release new version  '$HAMMR_VERSION'","head":"'$HAMMR_RELEASE_BRANCH'","base":"master"}' $GIT_API_ADDRESS/repos/$HAMMR_REPO/pulls)
if [ $STATUS -ne 201 ]; then
  release_failed "Cannot create the pull request to integrate $HAMMR_RELEASE_BRANCH into master"
fi

step_completed 5

clean_directory

terminated

echo "Tag created on github : $HAMMR_VERSION"
echo "Please edit it to create a github release or pre-release and add release note at $GIT_ADDRESS/$HAMMR_REPO/releases/tag/$HAMMR_VERSION"
echo "Hammr $HAMMR_VERSION should be available at https://pypi.python.org/pypi/hammr/$HAMMR_VERSION"
exit 0
