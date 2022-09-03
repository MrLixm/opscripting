# Katana launcher script

cd ..

KATANA_VERSION="3.6v5"
KATANA_HOME="C:\Program Files\Katana$KATANA_VERSION"
KATANA_TAGLINE="Opscripting DEV"

export PATH="$PATH;$KATANA_HOME\bin"
export KATANA_CATALOG_RECT_UPDATE_BUFFER_SIZE=1
export FNLOGGING_CONFIG=".\dev\KatanaResources\log.conf"
export KATANA_LOGGING_LEVEL_PYTHON="INFO"  # custom added in log.conf

export KATANA_USER_RESOURCE_DIRECTORY="Z:\dccs\katana\library\shelf0007\prefs"
export KATANA_RESOURCES="$KATANA_RESOURCES;.\dev\KatanaResources"

export PYTHONPATH="$PYTHONPATH;..\typing"
export PYTHONPATH="$PYTHONPATH;..\opscripting"
export PYTHONPATH="$PYTHONPATH;..\katanaingcore"

export LUA_PATH="$LUA_PATH;.\?.lua"
export LUA_PATH="$LUA_PATH;Z:\dccs\katana\library\shelf0006\lua\?.lua"  # llloger

"$KATANA_HOME\bin\katanaBin.exe"
