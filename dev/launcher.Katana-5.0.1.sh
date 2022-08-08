# Katana launcher script

KATANA_VERSION="5.0v1"
KATANA_HOME="C:\Program Files\Katana$KATANA_VERSION"
KATANA_TAGLINE="Opscripting DEV"

export PATH="$PATH;$KATANA_HOME\bin"
export KATANA_CATALOG_RECT_UPDATE_BUFFER_SIZE=1

export KATANA_USER_RESOURCE_DIRECTORY="Z:\dccs\katana\library\shelf0007\prefs"
export KATANA_RESOURCES="$KATANA_RESOURCES;Z:\packages-dev\opscripting\dev\KatanaResources"

export PYTHONPATH="$PYTHONPATH;Z:\packages-dev\typing"
export PYTHONPATH="$PYTHONPATH;Z:\packages-dev\opscripting"
export PYTHONPATH="$PYTHONPATH;Z:\packages-dev\katanaingcore"

export LUA_PATH="$LUA_PATH;Z:\packages-dev\opscripting\?.lua"
export LUA_PATH="$LUA_PATH;Z:\dccs\katana\library\shelf0006\lua\?.lua"

"$KATANA_HOME\bin\katanaBin.exe"
